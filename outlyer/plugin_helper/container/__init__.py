import os
import inspect
import importlib
import pkgutil
import docker


def is_container():
    if get_container_id():
        return True
    else:
        return False


def get_container_ip():
    return os.environ.get('CONTAINER_IP')


def get_container_id():
    return os.environ.get('CONTAINER_ID')


def _get_patch_modules():
    modules = []
    this_file = inspect.getfile(inspect.currentframe())
    this_package = inspect.getmodule(inspect.currentframe()).__name__

    cwd = os.path.dirname(os.path.abspath(this_file))

    for loader, module_name, ispkg in pkgutil.iter_modules([cwd]):
        mod = importlib.import_module(this_package + '.' + module_name)
        if hasattr(mod, 'patch') and hasattr(mod, 'unpatch') and\
           hasattr(mod, 'is_patched'):
            modules.append(mod)

    return modules


def patch_all():
    for mod in _get_patch_modules():
        getattr(mod, 'patch')()


def unpatch_all():
    for mod in _get_patch_modules():
        getattr(mod, 'unpatch')()
