from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from zope.component import getUtility
from zope.schema import Bytes, Iterable, Container, Text, getFieldsInOrder, Date, Datetime, Time
from .filefields import FILE_FIELD_TYPES
from .binarydiff import DexterityBinaryDiff
from .astextdiff import AsTextDiff
from .filelistdiff import DexterityFileListDiff

# TODO: Perhaps this can be replaced with some kind of Zope 3 style adaptation, in order to 
# provide better extensibility.
FIELDS_AND_DIFF_TYPES_RELATION = [
    (FILE_FIELD_TYPES, DexterityBinaryDiff),
    ((Iterable, Container), ListDiff),
    ((Date, Datetime, Time), AsTextDiff),
    ((Text, Bytes), TextDiff),
]
"""
Relates field types (`zope.schema.Field` subclasses) and "diff types"
(`Products.CMFEditions.BaseDiff.BaseDiff` subclasses). 

To find the best diff type for a field type this list will be searched until a match is found. 
If a match is not found then `FALL_BACK_DIFF_TYPE` is used.  
""" 

FALL_BACK_DIFF_TYPE = FieldDiff

# TODO: Perhaps this is not the best approach. Instead we should write a diff type which can handle
# lists of any kind of elements, providing extensibility mechanisms if we want to specialize the
# handling of certain value types. (rafaelbco)
VALUE_TYPES_AND_DIFF_TYPES_RELATION = [
    (FILE_FIELD_TYPES, DexterityFileListDiff),
]
"""
When a field is detected to be a list-like field we use this list in the same fashion as
`FIELDS_AND_DIFF_TYPES_RELATION` to try to find the best "diff type" according to the "value type"
of the field, i.e the type of the elements in the list. If a match is not found then a fall back
is used.
"""
 
# TODO: provide an easier way to exclude fields.
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
                if diff_type is ListDiff:
                    return self._get_diff_type_for_value_type(field.value_type) or diff_type
                        
                return diff_type
        
        return FALL_BACK_DIFF_TYPE
    
    def _get_diff_type_for_value_type(self, value_type):
        for (value_types, diff_type) in VALUE_TYPES_AND_DIFF_TYPES_RELATION:
            if isinstance(value_type, value_types):
                return diff_type
        
        return None
        
        