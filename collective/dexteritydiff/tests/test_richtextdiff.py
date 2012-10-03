from collective.dexteritydiff.richtextdiff import RichTextDiff
from plone.app.textfield.value import RichTextValue
from Products.CMFDiffTool.interfaces import IDifference

import unittest2 as unittest


class DummyType(object):
    def __init__(self, body):
        self.body = body


class RichTextDiffTestCase(unittest.TestCase):
    """Test RichTextDiff"""

    def test_inline_diff_same(self):
        value = RichTextValue(u'foo')
        diff = RichTextDiff(DummyType(value), DummyType(value), 'body')
        inline_diff = diff.inline_diff()

        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, True)
        self.assertEqual(inline_diff, u'foo ')

    def test_inline_diff_different(self):
        old_value = RichTextValue(u'foo')
        new_value = RichTextValue(u'foo bar')
        diff = RichTextDiff(
            DummyType(old_value), DummyType(new_value), 'body')

        inline_diff = diff.inline_diff()

        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, False)
        self.assertEqual(inline_diff, u'foo <span class="insert">bar </span> ')
