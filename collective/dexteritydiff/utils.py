from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from zope.component import getUtility

def title_or_value(vocabulary, value):
    """
    Given a `vocabulary` and a `value` in that vocabulary, return the corresponding title or 
    `value` if there is no title.
    """
    return vocabulary.getTerm(value).title or value

def get_schemas(obj):
    """Return a tuple (schema, additional_schemata)."""    
    fti = getUtility(IDexterityFTI, name=obj.portal_type)
    schema = fti.lookupSchema() 
    additional_schemata = getAdditionalSchemata(context=obj)
    return (schema, additional_schemata)
    
def get_field_object(obj, field_name):
    """
    Return the `zope.schema.Field` object corresponding to `field_name` in `obj`. Return `None` 
    if not found.
    """    
    (schema, additional_schemata) = get_schemas(obj)
    schemas = [schema] + list(additional_schemata)
    for s in schemas:
        field = s.get(field_name, None)
        if field is not None:
            return field
    
    return None     