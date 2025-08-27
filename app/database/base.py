"""
Base module for all models.
"""
import importlib
import json
import os

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase

from app.core.logger import log


class Base(DeclarativeBase):
    """
    Base class for all models.
    Necessary for alembic to work.
    All models now have a common ancestor.
    """

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the model.
        """
        data: dict = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }  # fmt: skip
        return (
            f"{self.__class__.__name__}"
            f"(\n{json.dumps(data, indent=2, default=str)}\n)"
        )  # fmt: skip


def import_models():
    """
    Automatically import all models in the models directory.
    """
    models_dir = os.path.join(os.path.dirname(__file__), "../models")
    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"app.models.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
            except ImportError as error:
                log.error(f"Failed to import {module_name}")
                raise error


import_models()
