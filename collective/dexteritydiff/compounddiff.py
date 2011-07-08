from Products.CMFDiffTool.BinaryDiff import BinaryDiff
from Products.CMFDiffTool.CMFDTHtmlDiff import CMFDTHtmlDiff
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from zope.app.content import queryContentType
from zope.component import getUtility, getUtility
from zope.schema import (Bytes, ASCII, BytesLine, ASCIILine, Choice, Field, Container, Iterable, 
    InterfaceField, Object, URI, Id, DottedName, Password, Dict, Datetime, Date, Timedelta, Text, 
    TextLine, Bool, Int, Float, Decimal, Time, SourceText, Tuple, List, Set, FrozenSet, getFieldsInOrder)

SIMPLE_FIELDS = (
    Field, Bool, Int, Float, Decimal, Datetime, Date, Timedelta, Time, Object, URI, Id, 
    DottedName, InterfaceField, Choice
)

FIELD_MAPPING = [
    ((Tuple, List, Set, FrozenSet,), ListDiff),
    ((Text, TextLine, SourceText), TextDiff),    
    ((Bytes,), BinaryDiff),
    (SIMPLE_FIELDS, FieldDiff),    
]
# Order must be more specific field types must be on top.
    

EXCLUDED_FIELDS = ('modification_date', 'changeNote')
class DexterityCompoundDiff(object):
    
    meta_type = 'Compound Diff for Dexterity types'
        
    def __init__(self, obj1, obj2, field, id1=None, id2=None):
        self.id1 = id1 or obj1.getId()
        self.id2 = id2 or obj2.getId()

                
        self._diffs = self._diff(obj1, obj2)
    
    def __getitem__(self, index):
        return self._diffs[index]

    def __len__(self):
        return len(self._diffs)

    def __iter__(self):
        return iter(self._diffs)

    def _diff(self, obj1, obj2):
        """
        Compute the differences between 2 objects.
        Return: a sequence of `IDifference` objects.
        """
        fti = getUtility(IDexterityFTI, name=obj1.portal_type)
        default_schema = fti.lookupSchema()
        
        diffs = self._diff_schema(obj1, obj2, default_schema, 'default')
        
        for schema in getAdditionalSchemata(context=obj1):        
            diffs.extend(self._diff_schema(obj1, obj2, schema, 'metadata'))
        
        return diffs
    
    def _diff_schema(self, obj1, obj2, schema, schema_name):
        """
        Compute the differences between 2 objects in respect to the given schema interface.
        Return: a sequence of `IDifference` objects.
        """
        return [
            self._diff_field(obj1, obj2, field, schema_name)
            for (name, field) in getFieldsInOrder(schema)
            if name not in EXCLUDED_FIELDS
        ]        
    
    def _diff_field(self, obj1, obj2, field, schema_name):
        """
        Compute the differences between 2 objects in respect to the given field.
        Return: an `IDifference` object.
        """        
        diff_type = self._get_diff_type(field)
        return diff_type(
            obj1, 
            obj2, 
            field.getName(), 
            id1=self.id1,
            id2=self.id2,
            field_name=field.getName(),
            field_label=field.title,
            schemata=schema_name
        )        
        
    
    def _get_diff_type(self, field):
        """
        Return a subclass of `Products.CMFEditions.BaseDiff.BaseDiff` suitable for the given 
        `zope.schema.Field` instance.
        """
        for (field_types, diff_type) in FIELD_MAPPING:
            if isinstance(field, field_types):
                return diff_type
        
        raise RuntimeError('Could not find a suitable diff type for the field %s' % field)              