
from .sau_fixed import get_primary_keys
from sqlalchemy import and_
from sqlalchemy.orm import object_session

__all__ = ["pk_join_expr", "rel_to_query"]

def pk_join_expr(table1, table2):
    cs1, cs2 = [get_primary_keys(t) for t in (table1, table2)]
    if len(cs1) != len(cs2):
        raise ValueError("not the same number of primary keys")
    return and_(*(cs1[k] == cs2[k]
                  for k in cs1.keys()))

def rel_to_query(obj, related_table, relationship_name):
    return object_session(obj).query(
        related_table).with_parent(obj, relationship_name)

