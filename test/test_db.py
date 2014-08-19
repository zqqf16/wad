#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys, time

from datetime import datetime

sys.path.append(os.path.join('../wad'))

import db

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        db.init_database('test.db')

    def tearDown(self):
        os.remove('test.db')

    def insert_entry(self, name, version, build):
        archive = db.Archive(name=name, identifier=name, version=version,
            build=build, path=name, date=datetime.now())
        archive.save()

    def test_query(self):
        _all_builds = ['1', '2', '3', '4', '5', '6']
        for build in _all_builds:
            self.insert_entry('test', '1.0', build)

        last_version = db.get_last_version()[0]
        self.assertEqual(last_version.build, '6')

    def test_multi_app(self):
        _all_builds = ['1', '2', '3', '4', '5', '6']
        for build in _all_builds:
            self.insert_entry('TestA', '1.0', build)
            self.insert_entry('TestB', '1.0', build)

        last_version = db.get_last_version()

        self.assertEqual(len(last_version), 2)
        self.assertEqual(last_version[0].build, '6')
        self.assertEqual(last_version[1].build, '6')

if __name__ == '__main__':
    unittest.main()
