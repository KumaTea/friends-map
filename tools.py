import re
from slimit import minify


def find_twitter_username(text):
    return re.findall(r'@[a-zA-Z0-9_]{1,15}', text)


def lower_list(original_list: list):
    return [x.lower() for x in original_list]


def remove_leading_at(original_list: list):
    return [x[1:] for x in original_list]


def slim_html(html):
    js_start_code = '<script type="text/javascript">\n'
    js_end_code = '\n</script>'

    html_before_js = html.split(js_start_code)[0] + js_start_code
    js_code = html.split(js_start_code)[1].split(js_end_code)[0]
    html_after_js = js_end_code + html.split(js_start_code)[1].split(js_end_code)[1]

    try:
        js_min = minify(js_code.replace('const', 'var'), mangle=True, mangle_toplevel=True)
    except:
        js_min = js_code

    return html_before_js + js_min + html_after_js
