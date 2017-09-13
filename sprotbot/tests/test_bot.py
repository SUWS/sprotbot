
from unittest import TestCase

from sprotbot.bot import determine_meeting_details
from datetime import datetime

class TestBot(TestCase):
    

    def test_1st(self):
        now = datetime(2017, 8, 1)
        e_string, e_type = determine_meeting_details(now)
        self.assertEqual(e_type, "meeting")

    def test_7th(self):
        now = datetime(2017, 9, 7)
        e_string, e_type = determine_meeting_details(now)
        self.assertEqual(e_type, "meeting")

    def test_8th(self):
        now = datetime(2017, 8, 8)
        e_string, e_type = determine_meeting_details(now)
        self.assertEqual(e_type, "workshop")

    def test_14th(self):
        now = datetime(2017, 9, 14)
        e_string, e_type = determine_meeting_details(now)
        self.assertEqual(e_type, "workshop")
