from django import template
register = template.Library()

@register.simple_tag
def lookup(dictionary, key):
	uuid_filename = dictionary.get (key,'')
	return dictionary.get(uuid_filename, '')

@register.simple_tag
def experiment_lookup(dictionary, key):
	return dictionary.get(key)