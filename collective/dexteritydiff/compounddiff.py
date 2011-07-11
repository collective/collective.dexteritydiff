from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from zope.component import getUtility
from zope.schema import Bytes, Iterable, Container, Text, getFieldsInOrder
from .filefields import FILE_FIELD_TYPES
from .binarydiff import DexterityBinaryDiff

FIELDS_AND_DIFF_TYPES_RELATION = [
    (FILE_FIELD_TYPES, DexterityBinaryDiff),
    ((Iterable, Container), ListDiff),
    ((Text, Bytes), TextDiff),
]
"""
Relates field types (`zope.schema.Field` subclasses) and "diff types"
(`Products.CMFEditions.BaseDiff.BaseDiff` subclasses). 

To find the best diff type for a field type this list will be searched until a match is found. 
If a match is not found then `FALL_BACK_DIFF_TYPE` is used.  
""" 

FALL_BACK_DIFF_TYPE = FieldDiff
    
EXCLUDED_FIELDS = ('modification_date', 'changeNote')
"""Names of fiels not to compare."""

class DexterityCompoundDiff(object):
    """Same as `Products.CMFDiffTool.ATCompoundDiff.ATCompoundDiff` but for Dexterity."""
    
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
        Compute the differences between 2 objects in respect to the given field 
        (`zope.schema.Field` instance).
        
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
        for (field_types, diff_type) in FIELDS_AND_DIFF_TYPES_RELATION:
            if isinstance(field, field_types):
                return diff_type
        
        return FALL_BACK_DIFF_TYPE       