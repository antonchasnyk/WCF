from django import template
from django.http import QueryDict

from WCF import settings

register = template.Library()


@register.filter(name='attr')
def attr(field, css):
    attrs = {}
    definition = css.split(',')
    for d in definition:
        if ':' not in d:
            attrs['class'] += d + ' '
        else:
            key, value = d.split(':')
            attrs[key] = value
    return field.as_widget(attrs=attrs)


@register.filter
def paginate(value, page):
    value, page = int(value), int(page)
    adjusted_value = value + ((page - 1) * settings.ITEMS_ON_PAGE)
    return adjusted_value


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key in kwargs:
        query[key] = kwargs[key]
    try:
        del query['csrfmiddlewaretoken']
    except KeyError:
        pass

    return query.urlencode()
