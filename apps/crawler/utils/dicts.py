
def attr_dict(iter, key, value):
    return {item[key]:item[value] for item in iter}


def make_dict_from_variables(*args):
    my_dict = {}
    for var_name in args:
        if var_name in globals():
            my_dict[var_name] = globals()[var_name]
    return my_dict

def recursive_dict_update(original_dict, additional_dict):
    for key, value in additional_dict.items():
        if isinstance(value, dict) and key in original_dict and isinstance(original_dict[key], dict):
            recursive_dict_update(original_dict[key], value)
        else:
            original_dict[key] = value