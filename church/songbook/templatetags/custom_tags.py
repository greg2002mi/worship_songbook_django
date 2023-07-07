from django import template

register = template.Library()

@register.simple_tag
def lookup_(var1, var2):
    return var1[var2]