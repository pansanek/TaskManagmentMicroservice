from collections import OrderedDict
import sqlalchemy as sa
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty

__all__ = ['get_columns', 'get_primary_keys']

def get_columns(mixed):
    """
    Return a collection of all Column objects for given SQLAlchemy
    object.

    The type of the collection depends on the type of the object to return the
    columns from.

    ::

        get_columns(User)

        get_columns(User())

        get_columns(User.__table__)

        get_columns(User.__mapper__)

        get_columns(sa.orm.aliased(User))

        get_columns(sa.orm.alised(User.__table__))


    :param mixed:
        SA Table object, SA Mapper, SA declarative class, SA declarative class
        instance or an alias of any of these objects
    """
    if isinstance(mixed, sa.sql.selectable.Selectable):
        return mixed.c
    if isinstance(mixed, sa.orm.util.AliasedClass):
        return OrderedDict((k, getattr(mixed, k))
                           for k in sa.inspect(mixed).mapper.columns.keys())
    if isinstance(mixed, sa.orm.Mapper):
        return mixed.columns
    if isinstance(mixed, InstrumentedAttribute):
        return mixed.property.columns
    if isinstance(mixed, ColumnProperty):
        return mixed.columns
    if isinstance(mixed, sa.Column):
        return [mixed]
    if not isclass(mixed):
        mixed = mixed.__class__
    return sa.inspect(mixed).columns

def get_primary_keys(mixed):
    """
    Return an OrderedDict of all primary keys for given Table object,
    declarative class or declarative class instance.

    :param mixed:
        SA Table object, SA declarative class or SA declarative class instance

    ::

        get_primary_keys(User)

        get_primary_keys(User())

        get_primary_keys(User.__table__)

        get_primary_keys(User.__mapper__)

        get_primary_keys(sa.orm.aliased(User))

        get_primary_keys(sa.orm.aliased(User.__table__))


    .. versionchanged: 0.25.3
        Made the function return an ordered dictionary instead of generator.
        This change was made to support primary key aliases.

        Renamed this function to 'get_primary_keys', formerly 'primary_keys'

    .. seealso:: :func:`get_columns`
    """
    return OrderedDict(
        (
            (key, column) for key, column in get_columns(mixed).items()
            if column.primary_key
        )
    )

