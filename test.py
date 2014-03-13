from twisted.trial import unittest
import irator
import os

character = os.environ.get('ACHAEA_CHARACTER', None)
password = os.environ.get('ACHAEA_PASSWORD', None)

class IratorTests(unittest.TestCase):

    def setUp(self):
        self.client = irator.Irator(character=character, password=password)

    def test_gamefeed(self):
        result = self.client.gamefeed()

        self.assertEqual(type(result), list)

    def test_orglogs(self):

        result = self.client.orglogs(org='targossas')

        self.assertEqual(type(result), list)

    def test_characters(self):

        result = self.client.characters()

        self.assertTrue('total' in result)

        result = self.client.characters('Jaiko')

        self.assertEqual(result, 'Jaiko Rian')

    def test_news(self):

        result = self.client.news()

        self.assertEqual(type(result), list)