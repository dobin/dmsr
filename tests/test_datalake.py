#!/usr/bin/env python

import unittest
from datalake import DataLake

class UtilsTest(unittest.TestCase):
    def test_datalake(self):
        dataLake = DataLake()

        agentname = "agent"
        pluginname = "plugin"
        data = "stuff"

        dataLake.push(agentname, pluginname, 3, data)
        d = dataLake.get(agentname, pluginname)
        self.assertEqual(d.data, data)

        d = dataLake.get(agentname, "bad")
        self.assertEqual(d, None)

        d = dataLake.get("bad", "bad")
        self.assertEqual(d, None)
