from sqlalchemy.ext.declarative import declarative_base, declared_attr
from collections.abc import Mapping

__all__ = [
    'merge_args',
    'merge_args_helper',
    'compute_table_args',
    'compute_mapper_args',
    'make_merge_args_class',
    'DELETE']

DELETE = ['DELETE']

def merge_args(argss):
    '''Merge each ``args`` from iterable ``argss``. First entry
takes priority.

Each ``args`` is either a dict or a list. The list can optionally end
in a dictionary. The dictionaries will be merged, and the lists will
be concatenated.

First entry wins. To remove a subsequent entry from the dictionary,
use ``DELETE`` as the key.
'''
    result = []
    result_dictionary = {}
    for args in argss:
        if callable(args):
            args = args() # resolve callable value by calling it

        # handle case where plain dict is passed as args
        if isinstance(args, Mapping):
            args = (args,)

        if args is None:
            # ignore None values
            pass
        elif len(args) and isinstance(args[-1], Mapping):
            # if there's a dictionary, it appears in the last position of
            # the iterable
            for key, value in args[-1].items():
                result_dictionary.setdefault(key, value)
            result.extend(args[:-1])
        else: # must be an iterable
            result.extend(args)

    for key, value in list(result_dictionary.items()):
        if value is DELETE:
            del result_dictionary[key]

    # unconditionally add dictionary
    result.append(result_dictionary)

    return tuple(result)

def merge_args_helper(cls, name, partial_name, this_name):
    '''Traverse inherited classes and merge their ``__X_args__``
attributes.

First merge from ``__this_X_args__`` (if it exists), then
``__partial_X_args__``. Then for each superclass: If
``__partial_X_args__`` exists, merge it.

Parameters
----------
name: str
    Name of usual attribute, i.e. ``__X_args__``.
partial_name: str
    Name of partial attribute, i.e. ``__partial_X_args__``.
this_name: str
    Name of usual attribute, i.e. ``__this_X_args__``.
'''
    def args_iter():
        mro = cls.mro()
        yield getattr(cls, this_name, None)
        yield getattr(cls, partial_name, None)
        for c in mro:
            for attribute_name in (partial_name,): # name
                superclass = super(c, cls)
                value = getattr(superclass, attribute_name, None)
                if value is not None:
                    yield value
                    break
    return merge_args(args_iter())

def compute_table_args(cls):
    return merge_args_helper(
        cls,
        '__table_args__' ,
        '__partial_table_args__',
        '__this_table_args__')

def compute_mapper_args(cls):
    return merge_args_helper(
        cls,
        '__table_mapper__' ,
        '__partial_mapper_args__',
        '__this_mapper_args__')[-1]

def make_merge_args_class(Base):

    class MergeArgs(Base):
        __abstract__ = True

        @declared_attr
        def __table_args__(cls):
            return compute_table_args(cls)

        @declared_attr
        def __mapper_args__(cls):
            return compute_mapper_args(cls)

    return MergeArgs

