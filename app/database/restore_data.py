#!/usr/bin/env python3
"""
Database restore script for Scenario API.

This script restores the database from a SQL dump file, completely replacing
the current database content. This operation is IRREVERSIBLE.

Usage:
    python app/database/restore_data.py [dump_file]

Args:
    dump_file (optional): Path to SQL dump file. Defaults to backup/scenario_dump.sql
"""

import os
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from app.core.settings import settings
from app.core.logger import log


def parse_database_url(database_url: str) -> dict:
    """
    Parse DATABASE_URL into connection parameters.

    Args:
        database_url: PostgreSQL connection URL

    Returns:
        dict: Connection parameters (host, port, database, username, password)

    Example:
        >>> params = parse_database_url("postgresql://user:pass@localhost:5432/dbname")
        >>> print(params['host'])  # localhost
    """
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],  # Remove leading slash
        'username': parsed.username,
        'password': parsed.password
    }


def confirm_restore_operation() -> bool:
    """
    Prompt user for confirmation before proceeding with restore.

    Returns:
        bool: True if user confirms, False otherwise
    """
    print("⚠️  WARNING: DATABASE RESTORE OPERATION")
    print("=" * 50)
    print("This operation will:")
    print("• DROP all existing tables and data")
    print("• RESTORE from the SQL dump file")
    print("• This action is IRREVERSIBLE")
    print("=" * 50)

    while True:
        response = input("Are you sure you want to continue? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def check_dump_file_exists(dump_file_path: Path) -> bool:
    """
    Check if the SQL dump file exists and is readable.

    Args:
        dump_file_path: Path to the SQL dump file

    Returns:
        bool: True if file exists and is readable
    """
    if not dump_file_path.exists():
        log.error(f"Dump file not found: {dump_file_path}")
        return False

    if not dump_file_path.is_file():
        log.error(f"Path is not a file: {dump_file_path}")
        return False

    if not os.access(dump_file_path, os.R_OK):
        log.error(f"Cannot read dump file: {dump_file_path}")
        return False

    return True


def restore_database(dump_file_path: Path) -> bool:
    """
    Restore database from SQL dump file using psql.

    Args:
        dump_file_path: Path to the SQL dump file

    Returns:
        bool: True if restoration successful, False otherwise
    """
    try:
        # Parse database connection parameters
        db_params = parse_database_url(settings.DATABASE_URL)

        log.info(f"Starting database restore from: {dump_file_path}")
        log.info(f"Target database: {db_params['database']} on {db_params['host']}")

        # Set PGPASSWORD environment variable for psql
        env = os.environ.copy()
        env['PGPASSWORD'] = db_params['password']

        # Build psql command
        psql_cmd = [
            'psql',
            f"--host={db_params['host']}",
            f"--port={db_params['port']}",
            f"--username={db_params['username']}",
            f"--dbname={db_params['database']}",
            '--quiet',
            '--file', str(dump_file_path)
        ]

        log.info("Executing database restore...")

        # Execute psql command
        result = subprocess.run(
            psql_cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )

        log.info("Database restore completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        log.error(f"Database restore failed with exit code {e.returncode}")
        log.error(f"Error output: {e.stderr}")
        return False

    except Exception as e:
        log.error(f"Unexpected error during database restore: {str(e)}")
        return False


def main():
    """
    Main function to orchestrate the database restore process.

    Steps:
    1. Parse command line arguments
    2. Check if dump file exists
    3. Get user confirmation
    4. Restore database
    """
    print("🔄 Scenario API - Database Restore Tool")
    print("=" * 40)

    # Determine dump file path
    if len(sys.argv) > 1:
        dump_file_path = Path(sys.argv[1])
    else:
        # Default to backup directory
        project_root = Path(__file__).parent.parent.parent
        dump_file_path = project_root / "app" / "database" / "backup" / "supabase_dump.sql"

    log.info(f"Using dump file: {dump_file_path}")

    # Check if dump file exists
    if not check_dump_file_exists(dump_file_path):
        log.error("Cannot proceed without a valid dump file")
        sys.exit(1)

    # Get user confirmation
    if not confirm_restore_operation():
        log.info("Database restore cancelled by user")
        sys.exit(0)

    # Perform database restore
    if restore_database(dump_file_path):
        print("✅ Database restore completed successfully!")
        log.info("Database restore operation finished")
    else:
        print("❌ Database restore failed!")
        log.error("Database restore operation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()