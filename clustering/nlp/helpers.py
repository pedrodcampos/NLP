from .common import __RESOURCES_FOLDER__
import os.path


def get_absolute_path():
    base_path = os.path.abspath(os.path.dirname(__package__))
    return "/".join([base_path, __package__])


def get_resource_path(file_name):
    package_path = get_absolute_path()
    return "/".join([package_path, __RESOURCES_FOLDER__, file_name])
