
# Configure the module to make importing of blueprints with the syntax of
# 'import blueprints -> blueprints.content' possible.
from .root import root
from .about import about
from .blog import blog
from .contact import contact
from .error import error
from .gallery import gallery
from .middleman import middleman
from .projects import projects
from .psa import psa
from .templates import templates

__all__ = [
    "about",
    "blog",
    "contact",
    "error",
    "gallery",
    "middleman",
    "projects",
    "psa",
    "templates"
]
