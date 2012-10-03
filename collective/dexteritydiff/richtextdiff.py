from Products.CMFDiffTool.CMFDTHtmlDiff import CMFDTHtmlDiff


class RichTextDiff(CMFDTHtmlDiff):
    """
    Specialization of `CMFDTHtmlDiff`to provide an inline diff visualization
    for plone.app.textfield.RichText field.
    """

    def _parseField(self, value, filename=None):
        """Parse the field using the raw value from RichTextValue."""
        if value is None:
            value = ''
        return CMFDTHtmlDiff._parseField(self, value.raw, filename)
