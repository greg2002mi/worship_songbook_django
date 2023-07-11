from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def lookup_(var1, var2):
    return var1[var2]

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
	
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
   
