#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Database'''

import os
import peewee

from datetime import datetime
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from playhouse.proxy import Proxy

_DEFAULT_DATABASE = 'wad.db'

_DATABASE_PROXY = Proxy()

class BaseModel(Model):
    '''Base Model'''
    class Meta:
        database = _DATABASE_PROXY

class Archive(BaseModel):
    '''Archive'''

    identifier = CharField()
    name = CharField()
    version = CharField()
    build = CharField(default='0')
    path = CharField()
    date = DateTimeField(formats='%Y-%m-%d %H:%M:%S', default=datetime.now())

    class Meta:
        order_by = ('-date',)

    def dict_format(self):
        '''Conver to dictionary'''

        return {'name': self.name, 'version':self.version, 'build':self.build,
                'date':self.date, 'path':self.path, 'id':self.id, #pylint: disable=E1101
                'identifier':self.identifier}

def init_database(db_name=_DEFAULT_DATABASE):
    '''Init database, if not exist, create a new one'''

    if not db_name:
        db_name = _DEFAULT_DATABASE

    database = SqliteDatabase(db_name, threadlocals=True)
    _DATABASE_PROXY.initialize(database)

    if not database.get_tables():
        database.create_tables([Archive])

def get_last_version(identifier=None):
    '''Get the last version'''

    query = Archive.select()
    if identifier:
        query = query.where(Archive.identifier == identifier)
    else:
        query = query.group_by(Archive.identifier)

    return [archive for archive in query]

def get_archives(identifier=None):
    '''Get all archives'''

    query = Archive.select()
    if identifier:
        query = query.where(Archive.identifier == identifier)

    return [archive.dict_format() for archive in query]

def get_archvie_by_id(archive_id):
    '''Get archive by id'''

    try:
        return Archive.get(Archive.id == archive_id)
    except:
        return None
