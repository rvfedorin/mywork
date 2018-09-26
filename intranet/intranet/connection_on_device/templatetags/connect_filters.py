from django import template

register = template.Library()

@register.filter('changetypeconnect')
def changetypeconnect(value):
    return value.as_widget(attrs={'is_hidden': True})