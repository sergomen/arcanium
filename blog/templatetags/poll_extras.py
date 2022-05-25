from django import template

register = template.Library()

@register.filter
def get_value(d, key):
    return d.get(key)

@register.filter(name='has_group')
def is_mod(user, group_name):
    return user.groups.filter(name=group_name).exists()