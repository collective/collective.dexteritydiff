from .astextdiff import AsTextDiff
from .i18n import MessageFactory as _
from zope.app.component.hooks import getSite

class BoolDiff(AsTextDiff):
    """
    Diff for boolean fields.
    
    Currently the only difference from `AsTextDiff` is that it allows for translation (i18n) of the 
    strings `True` and `False`.    
    """
    
    def _parseField(self, value, filename=None):        
        value = unicode('' if (value is None) else value)
        
        # In tests translation is not available, so we account for this case here.
        translate = getattr(getSite(), 'translate', None)
        if translate is not None:                
            value = translate(_(value))
        
        return AsTextDiff._parseField(self, value, filename)
    