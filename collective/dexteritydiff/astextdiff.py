from Products.CMFDiffTool.TextDiff import TextDiff

class AsTextDiff(TextDiff):
    """Specialization of `TextDiff` that convert any value to text to provide an inline diff.""" 
        
    def _parseField(self, value, filename=None):        
        if value is None:
            value = ''
        return TextDiff._parseField(self, str(value), filename)
    
  