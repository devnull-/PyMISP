#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from keys import url, key
import time

import unittest


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.misp = PyMISP(url, key, True, 'json')

    def _clean_event(self, event):
        event['Event'].pop('uuid', None)
        event['Event'].pop('timestamp', None)
        event['Event'].pop('date', None)
        event['Event'].pop('org', None)
        event['Event'].pop('orgc', None)
        event['Event'].pop('RelatedEvent', None)
        event['Event'].pop('publish_timestamp', None)
        if event['Event'].get('Attribute'):
            for a in event['Event'].get('Attribute'):
                a.pop('uuid', None)
                a.pop('event_id', None)
                a.pop('id', None)
                a.pop('timestamp', None)
        return event['Event'].pop('id', None)

    def new_event(self):
        event = self.misp.new_event(0, 1, 0, "This is a test")
        event_id = self._clean_event(event)
        self.assertEqual(event, {u'Event': {u'info': u'This is a test', u'locked': False,
                                            u'attribute_count': u'0', u'analysis': u'0',
                                            u'ShadowAttribute': [], u'published': False,
                                            u'distribution': u'0', u'Attribute': [], u'proposal_email_lock': False,
                                            u'threat_level_id': u'1'}})
        return int(event_id)

    def add_hashes(self, eventid):
        r = self.misp.get_event(eventid)
        event = r.json()
        event = self.misp.add_hashes(event, 'Payload installation', 'dll_installer.dll', '0a209ac0de4ac033f31d6ba9191a8f7a', '1f0ae54ac3f10d533013f74f48849de4e65817a7', '003315b0aea2fcb9f77d29223dd8947d0e6792b3a0227e054be8eb2a11f443d9', 'Fanny modules', False, 2)
        self._clean_event(event)
        to_check = {u'Event': {u'info': u'This is a test', u'locked': False,
                               u'attribute_count': u'3', u'analysis': u'0',
                               u'ShadowAttribute': [], u'published': False, u'distribution': u'0',
                               u'Attribute': [
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|0a209ac0de4ac033f31d6ba9191a8f7a',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|md5'},
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|1f0ae54ac3f10d533013f74f48849de4e65817a7',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|sha1'},
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|003315b0aea2fcb9f77d29223dd8947d0e6792b3a0227e054be8eb2a11f443d9',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|sha256'}],
                               u'proposal_email_lock': False, u'threat_level_id': u'1'}}
        self.assertEqual(event, to_check)

    def publish(self, eventid):
        r = self.misp.get_event(eventid)
        event = r.json()
        event = self.misp.publish(event)
        self._clean_event(event)
        to_check = {u'Event': {u'info': u'This is a test', u'locked': False,
                               u'attribute_count': u'3', u'analysis': u'0',
                               u'ShadowAttribute': [], u'published': True, u'distribution': u'0',
                               u'Attribute': [
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|0a209ac0de4ac033f31d6ba9191a8f7a',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|md5'},
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|1f0ae54ac3f10d533013f74f48849de4e65817a7',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|sha1'},
                                   {u'category': u'Payload installation', u'comment': u'Fanny modules',
                                    u'to_ids': False, u'value': u'dll_installer.dll|003315b0aea2fcb9f77d29223dd8947d0e6792b3a0227e054be8eb2a11f443d9',
                                    u'ShadowAttribute': [], u'distribution': u'2', u'type': u'filename|sha256'}],
                               u'proposal_email_lock': False, u'threat_level_id': u'1'}}
        self.assertEqual(event, to_check)

    def delete(self, eventid):
        event = self.misp.delete_event(eventid)
        event.json()

    def test_all(self):
        eventid = self.new_event()
        time.sleep(1)
        self.add_hashes(eventid)
        time.sleep(1)
        self.publish(eventid)
        self.delete(eventid)

if __name__ == '__main__':
    unittest.main()
