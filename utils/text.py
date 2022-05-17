def replace_text(dct, text):
    if type(dct) == dict:
        for key, value in dct.items():
            text = text.replace(f'%{key}%', str(value))
    return text


def sanitise_dict(arg):
    data = ''
    clean = lambda x: x.replace('{', '').replace('}', '').strip()
    for pair in arg.split(','):
        kv = pair.split(':')
        if len(kv) < 2:
            continue
        k = clean(kv[0])
        v = clean(':'.join(kv[1:]))
        # omit kv if value is empty
        if len(v.replace('"', '')) == 0:
            continue
        data += f',{k}:{v}' if data else f'{k}:{v}'
    return data


def sanitise_list(arg):
    data = ''
    clean = lambda x: x.replace('[', '').replace(']', '').replace('"', '').strip()
    for value in arg.split(','):
        v = clean(value)
        if len(v) == 0:
            data += f',None' if data else f'None'
        elif str(v)[:1] in ['<', '>', '=']:
            data += f',"{v}"' if data else f'"{v}"'
        else:
            data += f',{v}' if data else f'{v}'
    # this clause won't be fulfilled if data is None,Object
    if data == 'None':
        data = ''
    return data
