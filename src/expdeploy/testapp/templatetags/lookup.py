from django import template
register = template.Library()

@register.simple_tag
def lookup(dictionary, key):
	uuid_filename = dictionary.get (key,'')
	return dictionary.get(uuid_filename, '')