FILE_FIELD_TYPES = []

try:
    import plone.namedfile.field as field
    FILE_FIELD_TYPES.extend([field.NamedFile, field.NamedImage])
    
    if field.HAVE_BLOBS:
        FILE_FIELD_TYPES.extend([field.NamedBlobFile, field.NamedBlobImage])        
except ImportError:
    pass


FILE_FIELD_TYPES = tuple(FILE_FIELD_TYPES)
        