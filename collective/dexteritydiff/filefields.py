import hashlib

FILE_FIELD_TYPES = []

try:
    from plone.namedfile import field 
    FILE_FIELD_TYPES.extend([field.NamedFile, field.NamedImage])
    
    if field.HAVE_BLOBS:
        FILE_FIELD_TYPES.extend([field.NamedBlobFile, field.NamedBlobImage])   
except ImportError:
    pass

FILE_FIELD_TYPES = tuple(FILE_FIELD_TYPES)
        
def named_file_as_str(f):
    return '' if f is None else '%s (%d bytes)' % (f.filename, len(f.data))
    
#    return 'Filename: %s\nMD5: %s' % (
#        ('-', '-') if f is None
#        else (f.filename, hashlib.md5(f.data).hexdigest())
#    )        

def is_same(old_data, old_filename, new_data, new_filename):
    if old_data != new_data:
        return False
    
    if (old_filename is not None) and (new_filename is not None):
        return old_filename == new_filename
    
    return True    