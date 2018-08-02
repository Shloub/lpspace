br = "<br />\n"


def indent(s):
    lines = s.splitlines()
    lines = ["    " + l for l in lines]
    return "\n".join(lines)


def form(txt, button, method="get"):
    # txt = indent(txt)
    template = """<form method="{method}">
{txt}
<br />
<input type="submit" value="{button}">
</form>
"""
    return template.format(method=method, txt=txt, button=button)


def myinput(name, mytype="text", mymin=None, mymax=None, value=None,
            checked=False):
    d = {'min': mymin, 'max': mymax, 'value': value}
    s = " ".join(i + '="' + d[i] + '"' for i in d if d[i])
    ch = ' checked' if checked else ''
    res = (name + ': <input name="' + name + '" type="' + mytype + '" '
           + s + ch + '>\n')
    return res


def page(title, body, color=None):
    # body = indent(body)
    style = " style='background-color:" + color + "'" if color else ""
    template = """<!DOCTYPE html>
<html lang="en">
<head>
<title>
{title}
</title>
</head>
<body{style}>
{body}
</body>
</html>
"""
    return template.format(title=title, style=style, body=body)


def select(name, options, selected=None):
    s = name + ': <select name="' + name + '">\n'
    for option in options:
        sel = ''
        if option == selected:
            sel = ' selected="selected"'
        template = '<option value="{option}"{sel}>{option}</option>\n'
        s += template.format(option=option, sel=sel)
    s += "</select>\n"
    return s


def textarea(name=None, rows=None, cols=None, txt=""):
    d = {'name': name, 'rows': rows, 'cols': cols}
    s = " ".join(i+'="'+d[i]+'"' for i in d if d[i])
    template = """<textarea {s}>
{txt}
</textarea>
"""
    return template.format(s=s, txt=txt)
