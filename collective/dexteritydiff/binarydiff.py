from Products.CMFDiffTool.BinaryDiff import BinaryDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from .filefields import named_file_as_str, is_same
from plone.namedfile import NamedFile

class DexterityBinaryDiff(BinaryDiff):
    
    def __init__(self, obj1, obj2, field, id1=None, id2=None, field_name=None, field_label=None, 
        schemata=None):
        
        self.field = field
        self.label = field_label or field
        self.schemata = schemata or 'default'
        self.field_name = field_name or field
        
        old_field = getattr(obj1, field)
        new_field = getattr(obj2, field)
                
        self.oldValue = getattr(old_field, 'data', None)
        self.newValue = getattr(new_field, 'data', None)
                
        self.id1 = id1 or getattr(obj1, 'getId', lambda: None)()
        self.id2 = id2 or getattr(obj2, 'getId', lambda: None)()
                
        self.oldFilename = getattr(old_field, 'filename', None)
        self.newFilename = getattr(new_field, 'filename', None)
        
        self.same = is_same(self.oldValue, self.oldFilename, self.newValue, self.newFilename)
            
    def _parseField(self, value, filename=None):
        return [
            '' if (value is None)
            else named_file_as_str(NamedFile(data=value, filename=filename)) 
        ]         
    
    def inline_diff(self):
        css_class = 'InlineDiff'
        old = self._parseField(self.oldValue, self.oldFilename)[0]
        new = self._parseField(self.newValue, self.newFilename)[0]
            
        return '' if self.same else self.inlinediff_fmt % (css_class, old, new)