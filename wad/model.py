#!/usr/bin/env python

'''Model'''

import json


class Archive(object):

    '''Archive'''

    _instances = None
    _database = 'archives.json'

    def __init__(self, name, identifier, version, build):
        self.name = name
        self.identifier = identifier
        self.version = version
        self.build = build

    def __str__(self):
        return self.name

    def encode(self):
        '''Encode to dict'''
        return {'name': self.name,
                'id': self.identifier,
                'version': self.version,
                'build': self.build}

    @classmethod
    def decode(cls, dict_value):
        '''Decode from dict'''
        return cls(dict_value['name'],
                   dict_value['id'],
                   dict_value['version'],
                   dict_value['build'])

    @classmethod
    def load(cls, force=False):
        '''Load archives from database'''

        if cls._instances != None and not force:
            return

        try:
            with open(cls._database, 'r') as db_file:
                cls._instances = {}
                for identifier, ins in json.load(db_file).items():
                    cls._instances[identifier] = cls.decode(ins)
        except IOError:
            pass

        if cls._instances == None:
            cls._instances = {}
            cls.save()

    @classmethod
    def save(cls):
        '''Save archives to database'''

        with open(cls._database, 'w') as db_file:
            collections = {id: ins.encode()
                           for (id, ins) in cls._instances.items()}
            json.dump(collections, db_file)

    @classmethod
    def all(cls):
        '''Get all archives'''

        cls.load()
        return cls._instances

    @classmethod
    def get(cls, identifier):
        '''Get the archive with the given id'''

        cls.load()
        return cls._instances.get(identifier, None)

    @classmethod
    def add(cls, instance):
        '''Add an archive'''

        cls.load()
        cls._instances[instance.identifier] = instance

    @classmethod
    def delete(cls, identifier):
        '''Delete an archive from database'''

        cls.load()
        cls._instances.pop(identifier)
