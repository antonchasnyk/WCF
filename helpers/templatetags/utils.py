from django.template import Library
register = Library()


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
