from .auth import auth_bp
from .recipes import recipes_bp
from .search import search_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'recipes_bp', 'search_bp', 'admin_bp']
