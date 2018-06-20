from argparse import ArgumentTypeError
from importlib import import_module


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]


def imported_argument(full_class_name):
    module_name, class_name = full_class_name.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError as ex:
        raise ArgumentTypeError("can't import " + module_name)
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ArgumentTypeError("attribute {} not found on module {}".format(
            class_name,
            module_name))