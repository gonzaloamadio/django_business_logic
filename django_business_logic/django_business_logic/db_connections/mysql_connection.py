# -*- coding: utf-8 -*-
#import the MySQLdb module
import MySQLdb
from functools import wraps
import logging
log = logging.getLogger(__name__)
from datetime import datetime

def _safely_do(func):
    @wraps(func)
    def do_or_log(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except MySQLdb.DatabaseError as exception:
            log.error(datetime.now())
            log.error(exception.args)
            log.error(exception)
            raise
        except Exception as e:
            log.error(datetime.now())
            log.error(e)
            raise
        #finally:
        #    if self._connection:
        #        self.rollback()
        #        self._connection.close()
    return do_or_log


class sms_db_access(object):

    def __init__(self, host, database, username, password):
        self._host = host
        self._database = database
        self._user = username
        self._pass = password
        try:
            self._connection = MySQLdb.connect(passwd=self._pass,db=self._database, host=self._host,user=self._user)
            self._cr = self._connection.cursor()
        except Exception as err:
            self._connection = None
            self._cr = None
            raise

    @_safely_do
    def do_query(self, query, params=(), as_dict=False):
        return self._do_query(query, params=params)

    @_safely_do
    def do_execute(self, query, params=()):
        self._cr.execute(query, params)

    @_safely_do
    def _do_query(self, query, params=()):
        self.do_execute(query, params)
        return self._cr.fetchall() or []

    def close(self):
        self._connection.close()



