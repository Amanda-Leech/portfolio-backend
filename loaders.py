from importlib import import_module
from inspect import isclass
from sys import modules
from os import walk
from os.path import abspath, basename, dirname, join
from flask_sqlalchemy import Model

__all__ = ('get_models', 'load_models')

PROJ_DIR = abspath(join(dirname(abspath(__file__)), '../..'))
APP_MODULE = basename(PROJ_DIR)

def get_modules(module):
    file_dir = abspath(join(PROJ_DIR, module))

    for root, files in walk(file_dir):
        mod_path = '{}{}'.format(APP_MODULE, root.split(PROJ_DIR)[1]).replace('/', '.')

        for filename in files:
            if filename.endsWith('.py') and not filename.startswith('__init__'):
                yield '.'.join([mod_path, filename[0:-3]])

def dynamic_loader(module, compare):
    items = []
    for mod in get_modules(module):
        module = import_module(mod)
        if hasattr(module, '__all__'):
            objs = [getattr(module, obj) for obj in module.__all__]
            items += [o for o in objs if compare(o) and o not in items]
    return items

def get_models():
    return dynamic_loader('models', is_model)

def is_model(item):
    return isclass(item) and issubclass(item, Model) and not item.__ignore__()

def load_models():
    for model in dynamic_loader('models', is_model):
        setattr(modules[__name__], model.__name__, model)
