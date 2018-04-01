import pkg_resources
pkg_resources.declare_namespace(__name__)
__version__ = pkg_resources.get_distribution(__package__).version
