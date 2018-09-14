from django import template

register = template.Library()

@register.filter('addclass')
def addclass(value, _class):
    return value.as_widget(attrs={'class': _class})