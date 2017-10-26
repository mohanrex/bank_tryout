"""
    Tiny DB Engine Implementation
"""

from copy import deepcopy
from tinydb import Query, TinyDB, where
from tinydb.storages import MemoryStorage

class TinyDBEngine(object):
    "Engine for Tiny db"
    def __init__(self, tablename="default"):
        """Initialises the engine for tinydb
        """
        self._tdb = TinyDB('data/' + tablename + '.json', default_table=tablename)
        self._query = Query()

    def clear_db(self):
        """Clears all the tables in the database"""
        self._tdb.purge_tables()

    def add_record(self, idx, values):
        """Adds a new record to the database
        """
        return self._tdb.insert({
            "idx": idx,
            "values": values
        })

    def update_record(self, idx, update_attr):
        """Updates a record"""
        self._tdb.update(update_attr, self._query.idx == idx)

    def delete_record(self, idx):
        self._tdb.remove(where('idx') == idx)

    def get_record_by_id(self, idx):
        "Returns a particular row"
        return self._tdb.get(self._query.idx == idx)

    def get_records(self):
        "Returns a all row"
        return self._tdb.all()

ACCOUNTS_DB = TinyDBEngine(tablename="Accounts")
SECRET_DB = TinyDBEngine(tablename="Secrets")