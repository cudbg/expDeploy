from django import template
register = template.Library()
import socket

@register.filter
def is_published(dictionary,value): # Only one argument.
    """Converts a string into all lowercase"""
    console.log(dictionary)
    return True

@register.simple_tag
def lookup(dictionary, key):
	uuid_filename = dictionary.get (key,'')
	return dictionary.get(uuid_filename, '')

@register.simple_tag
def explink(dictionary, key):
	return dictionary.get(key)

@register.simple_tag
def expfullink(dictionary, key):
	return "https://www.gpaas.xyz" + str(dictionary.get(key))

@register.simple_tag
def formlookup(dictionary, experiment, form):
	inner_formdict = dictionary.get(experiment)
	return inner_formdict.get(form)

@register.simple_tag
def publishlookup(dictionary, key):
	return dictionary.get(key)

