from .common import __RESOURCES_FOLDER__, __DATA_FODLER__, __OUTPUT_FOLDER__
import os.path


def get_app_dir():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_package_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_resource_dir():
    return "/".join([get_package_dir(), __RESOURCES_FOLDER__])


def get_resource_file(filename):
    return "/".join([get_resource_dir(), filename])


def get_output_dir():
    return "/".join([get_app_dir(), __OUTPUT_FOLDER__])


def get_output_file(filename):
    return "/".join([get_app_dir(), __OUTPUT_FOLDER__, filename])
