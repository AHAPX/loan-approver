from django import template


register = template.Library()


@register.filter('element')
def element(value, name):
    if value in ['', None]:
        return f'<{name}/>'
    try:
        value = value.strip()
    except:
        pass
    return f'<{name}>{value}</{name}>'
    
