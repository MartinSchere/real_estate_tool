from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    try:
        url = '?{}={}'.format(field_name, value)
        if urlencode:
            querystring = urlencode.split('&')
            filtered_querystring = filter(
                lambda p: p.split('=')[0] != field_name, querystring)
            encoded_querystring = '&'.join(filtered_querystring)
            url = '{}&{}'.format(url, encoded_querystring)
    except Exception as e:
        print(e)
    return url
