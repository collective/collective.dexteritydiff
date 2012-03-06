from Products.CMFDiffTool.TextDiff import TextDiff

class AsTextDiff(TextDiff):
    """
    Specialization of `TextDiff` that converts any value to text in order to provide an 
    inline diff visualization.
    """ 
        
    def _parseField(self, value, filename=None):        
        if value is None:
            value = ''
        return TextDiff._parseField(self, str(value), filename)
    
  