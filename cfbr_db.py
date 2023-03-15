import sqlite3
from constants import DB
from flask import g
from logger import Logger

###############################################################
#
# Database -- taken from https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/
#
###############################################################
log = Logger.getLogger(__name__)

class Db:
    local_db = None
    local_db_fname = None

    @staticmethod
    def get_db(fname=None):
        # Default to Flask context when it's available. Everything else here is for testing.  Sheesh.
        if g:
            db = getattr(g, '_database', None)
            if db is None:
                db = g._database = sqlite3.connect(DB)
        elif fname and Db.local_db_fname:
            if fname == Db.local_db_fname:
                # They're requesting what's already opened, I'll allow it
                db = Db.local_db
            else:
                # They want to open a new file.  Note it and allow it
                log.warn(f"Opening new DB {fname} when DB {Db.local_db_filename} was already open")
                Db.local_db.close()
                db = Db.local_db = sqlite3.connect(fname)
                Db.local_db_fname = fname
        elif fname and not Db.local_db_fname:
            # Open the db file with the filename provided
            db = Db.local_db = sqlite3.connect(fname)
            Db.local_db_fname = fname
        elif not fname and Db.local_db:
            # Return the open local db
            db = Db.local_db
        else:
            # No filename, no Flask, no already-open DB.  Oops.
            raise ValueError("Not running in a flask context and no filename provided to get_db")
        return db

    @staticmethod
    def close_connection(exception=None):
        if g:
            db = getattr(g, '_database', None)
        elif Db.local_db:
            db = Db.local_db
        else:
            raise ValueError("Not running in a flask context and no local_db opened in close_connection")

        if db is not None:
            db.close()
            Db.local_db_fname = None
