from sqlalchemy import event
'''
pysqlite has long-standing issues with transactions, some of which have known
workarounds. Rather than make those workarounds the default, the sqlalchemy devs
have instead chosen to make the broken behaviour the default.

http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl

Fucking fuck.
'''

__all__ = ['sqlalchemy_pysqlite_fixup']

def sqlalchemy_pysqlite_fixup(engine):
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, "begin")
    def do_begin(conn):
        # emit our own BEGIN
        conn.execute("BEGIN")

