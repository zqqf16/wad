#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from peewee import *

db = SqliteDatabase('archives.db')

class BaseModel(Model):
    class Meta:
        database = db

class Archive(BaseModel):
    name = CharField()
    identifier = CharField()
    version = CharField(default='')
    build = CharField(default='')
    file_name = CharField()
    date = DateTimeField(default=datetime.now())
    size = FloatField()

def init_database():
    Archive.create_table()

if __name__ == '__main__':
    init_database()
