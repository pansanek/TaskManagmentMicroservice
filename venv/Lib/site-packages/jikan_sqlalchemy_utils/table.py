from sqlalchemy import Index
from sqlalchemy.ext.associationproxy import association_proxy, _AssociationList

__all__ = ['repr_helper', 'index']

def repr_helper(name, kv, ignore_empty=False, ignore_None=True):
    r = []
    for k,v in kv:
        if isinstance(v, bool):
            if v == True:
                r.append(k)
        else:
            if (ignore_empty and
                isinstance(v, (list, _AssociationList)) and not len(v)):
                continue
            if ignore_None and v is None:
                continue
            r.append("{}={!r}".format(k,v) if k is not None else
                     "{!r}".format(v))
    return '<{} {}>'.format(name, ' '.join(r))

def index(cls, name, *args, **kwargs):
    if not (args or kwargs):
        args = (name,)
    return Index('__'.join(('index', cls.__tablename__, name)),
                 *args, **kwargs)
