from plone.namedfile.interfaces import INamedFile
from .filefields import named_file_as_str, is_same
from Products.CMFDiffTool.ListDiff import ListDiff
from Products.CMFDiffTool.TextDiff import TextDiff
from plone.namedfile import NamedFile

def make_lists_same_length(s1, s2, dummy_element):
    if len(s1) > len(s2):
        s2 += [dummy_element] * (len(s1) - len(s2))
    if len(s2) > len(s1):
        s1 += [dummy_element] * (len(s2) - len(s1))       

class DexterityFileListDiff(ListDiff):
    """Specialization of `ListDiff` to handle lists of files better."""
    
    same_fmt = """<div class="%s">%s</div>"""
    inlinediff_fmt = TextDiff.inlinediff_fmt
    
    def __init__(self, obj1, obj2, field, id1=None, id2=None, field_name=None, field_label=None, 
        schemata=None):
        
        ListDiff.__init__(self, obj1, obj2, field, id1, id2, field_name, field_label, schemata)
        
        old_values = list(self.oldValue or [])
        new_values = list(self.newValue or [])
        
        self.same = True        
        if len(old_values) != len(new_values):
            self.same = False
        else:                
            for (old, new) in zip(old_values, new_values):
                if not is_same(old.data, old.filename, new.data, new.filename):
                    self.same = False
                    break
    
    def _parseField(self, value, filename=None):   
        value = value or []     
        return [named_file_as_str(f) for f in value]                        
                        
    def inline_diff(self):        
        if self.same:
            return None
        
        css_class = 'InlineDiff'
                
        old_reprs = self._parseField(self.oldValue, None)
        new_reprs = self._parseField(self.newValue, None)
        
        old_data = [
            {'repr': repr, 'data': value.data, 'filename': value.filename}
            for (repr, value) in zip(old_reprs, self.oldValue or [])
        ]
        new_data = [
            {'repr': repr, 'data': value.data, 'filename': value.filename}
            for (repr, value) in zip(new_reprs, self.newValue or [])
        ]
                
        dummy_dict = {'repr': '', 'data': None, 'filename': None}
        make_lists_same_length(old_data, new_data, dummy_dict) 
        
        is_same_dict = lambda d1, d2: is_same(
            d1['data'], d1['filename'], d2['data'], d2['filename']
        ) 
        
        return '\n'.join([
            (
                (self.same_fmt % (css_class, d_old['repr'])) if is_same_dict(d_old, d_new)
                else self.inlinediff_fmt % (css_class, d_old['repr'], d_new['repr'])
            ) for (d_old, d_new) in zip(old_data, new_data)                    
        ])    