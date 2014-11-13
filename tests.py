import unittest
import locale
from time import gmtime, strftime
from datetime import datetime
from rfeed import *

class SerializableTestCase(unittest.TestCase):

	def test_date(self):
		self.assertEquals('Thu, 13 Nov 2014 08:00:00 GMT', Serializable().date(datetime.datetime(2014, 11, 13, 8, 0, 0)))
		self.assertEquals('Mon, 01 Dec 2014 10:22:15 GMT', Serializable().date(datetime.datetime(2014, 12, 1, 10, 22, 15)))

	def test_date_returns_none_if_date_is_none(self):
		self.assertIsNone(Serializable().date(None))

class FeedTestCase(unittest.TestCase):

	def test_required_elements(self):

		self.assertTrue(self._element('title', 'This is a sample title') in Feed('This is a sample title', '', '').rss())
		self.assertTrue(self._element('link', 'https://www.google.com') in Feed('', 'https://www.google.com', '').rss())
		self.assertTrue(self._element('description', 'This is a sample description') in Feed('', '', 'This is a sample description').rss())

	def test_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = None, link = '', description = '')
		self.assertTrue('title' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = None, description = '')
		self.assertTrue('link' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = '', description = None)
		self.assertTrue('description' in str(cm.exception))

	def test_optional_elements_are_present(self):
		self.assertTrue(self._element('language', 'en-us') in Feed('', '', '', language = 'en-us').rss())
		self.assertTrue(self._element('copyright', 'Copyright 2014') in Feed('', '', '', copyright = 'Copyright 2014').rss())
		self.assertTrue(self._element('managingEditor', 'John Doe') in Feed('', '', '', managingEditor = 'John Doe').rss())
		self.assertTrue(self._element('webMaster', 'john@doe.com') in Feed('', '', '', webMaster = 'john@doe.com').rss())
		self.assertTrue(self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0)).rss())
		self.assertTrue(self._element('lastBuildDate', 'Mon, 01 Dec 2014 10:22:15 GMT') in Feed('', '', '', lastBuildDate = datetime.datetime(2014, 12, 1, 10, 22, 15)).rss())
		self.assertTrue(self._element('generator', 'Name goes here') in Feed('', '', '', generator = 'Name goes here').rss())

	def test_if_generator_not_specified_use_default_value(self):
		# I'm partially checking for the element because the value includes the version number and
		# changing it will break the test. By just doing a partial match, I make sure the test keeps
		# working in future versions as well.
		self.assertTrue('<generator>rfeed v' in Feed('', '', '').rss())		

	def _element(self, element, value):
		return '<' + element + '>' + value + '</' + element + '>'

if __name__ == '__main__':
    unittest.main()