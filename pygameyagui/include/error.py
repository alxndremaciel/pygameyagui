def raise_type_error(_var, _var_name, _type):
    if isinstance(_type, str):
        _type_str = _type
    elif isinstance(_type, list):
        if len(_type) == 1:
            _type_str = _type[0]
        if len(_type) > 1:
            _type_str = ', '.join(_type[:-1]) + f' or {_type[-1]}'
    else:
        raise SyntaxError('It was not possible to parse the _type argument in raise_type_error')
    _given = str(type(_var)).split('\'')[1]
    raise TypeError(f'{_var_name} value must be of type {_type_str}. Instead, type {_given} was given.')

def raise_value_error(_error_msg):
    if isinstance(_error_msg, str):
        raise ValueError(_error_msg)
    else:
        raise_type_error(_error_msg, '_error_msg', 'string')