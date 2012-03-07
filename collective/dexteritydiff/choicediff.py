from .astextdiff import AsTextDiff
from .utils import get_field_object, title_or_value

class ChoiceDiff(AsTextDiff):
    """
    Diff for choice fields.
    
    It's implemented as an specialization of `AsTextDiff`. The difference is that this class 
    tries to obtain the title corresponding to the value from the vocabulary associated with
    the field in order to provide an user-friendlier inline diff to the user.        
    """
    def __init__(self, obj1, obj2, field, id1=None, id2=None, field_name=None, field_label=None, 
        schemata=None):
        
        AsTextDiff.__init__(self, obj1, obj2, field, id1, id2, field_name, field_label, schemata)                
        
        self._vocabulary = None
        
        # Tries to find a vocabulary. First we need to find an object and the field instance. 
        obj = obj1 if (obj1 is not None) else obj2
        field_name = field_name or field
        field_instance = (
            get_field_object(obj, field_name) if (obj and field_name) 
            else None
        )
        
        if field_instance is not None:
            # Binding the field to an object will construct the vocabulary using a factory if 
            # necessary.                        
            self._vocabulary = field_instance.bind(obj).vocabulary
        
    def _parseField(self, value, filename=None):      
        if value is None:
            value = ''
        elif self._vocabulary is not None:
            value = title_or_value(self._vocabulary, value)
        
                
        return AsTextDiff._parseField(self, value, filename)

    