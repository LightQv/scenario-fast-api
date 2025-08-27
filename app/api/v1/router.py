"""
This file contains the main router that includes all the other routers.
It automatically imports all the routers in the `/routes` directory.
"""
import pkgutil
import importlib
from fastapi import APIRouter

from app.api.v1 import __name__ as route_package_name

main_router = APIRouter()

package = importlib.import_module(route_package_name)

for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f"{route_package_name}.{module_name}")
    if hasattr(module, "router"):
        main_router.include_router(
            module.router,
            prefix=f"/{module_name.replace('_', '-')}",
            tags=[module_name.capitalize()]
        )
