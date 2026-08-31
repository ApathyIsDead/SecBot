from .check import router as check_router
from .hash import router as hash_router
from .password import router as password_router
from .start import router as start_router

routers = [start_router, password_router, hash_router, check_router]
