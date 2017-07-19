import sqlite3

from sample.logged_event import Event


def record_event_sqlite(event: Event):
    """ records event in a local sqlite db """
    # TODO finish this
    raise NotImplementedError

    conn = sqlite3.connect(sys.path[0] + '/data/time.db')
    c = conn.cursor()

    # check if events table exists and create one if needed
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if c.fetchone() is None:
        init_sqlite_db(conn)


def init_sqlite_db(conn: sqlite3.Connection):
    """ creates a table with the desired schema for storing events """
    conn.execute("(CREATE TABLE events (timestamp text, tz text, activity_type text)")
    conn.commit()
