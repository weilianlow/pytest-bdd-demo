import json


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


def sanitise_data(data, delete_empty_string=False, delete_none=False, delete_empty_string_key=True,
                  delete_empty_none_key=True, output_type='auto'):
    def sanitise_child(obj):
        if isinstance(obj, list):
            index = 0
            while index < len(obj):
                if isinstance(obj[index], list) or isinstance(obj[index], dict):
                    obj[index] = sanitise_child(obj[index])
                elif obj[index] is None and delete_none:
                    obj = obj[:index] + obj[index + 1:]
                    continue
                elif obj[index] == '' and delete_empty_string:
                    obj = obj[:index] + obj[index + 1:]
                    continue
                index += 1
        elif isinstance(obj, dict):
            pop_keys = []
            for k, v in obj.items():
                if isinstance(v, list) or isinstance(v, dict):
                    v = sanitise_child(v)
                elif v is None and delete_empty_none_key:
                    pop_keys.append(k)
                elif v == '' and delete_empty_string_key:
                    pop_keys.append(k)
            for k in pop_keys:
                obj.pop(k)
        return obj

    if output_type == 'str':
        if isinstance(data, list) or isinstance(data, dict):
            return json.dumps(sanitise_child(data))
        elif isinstance(data, str):
            return json.dumps(sanitise_child(eval(data)))
    elif output_type == 'raw':
        if isinstance(data, list) or isinstance(data, dict):
            return sanitise_child(data)
        elif isinstance(data, str):
            return sanitise_child(eval(data))
    else:
        if isinstance(data, list) or isinstance(data, dict):
            return sanitise_child(data)
        elif isinstance(data, str):
            return json.dumps(sanitise_child(eval(data)))
