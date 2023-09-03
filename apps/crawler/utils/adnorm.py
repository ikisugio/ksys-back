import re
import jaconv
from normalize_japanese_addresses import normalize


def replace_address(input_string):
    convert_map = { 'O': '0', '一': '1', '二': '2',
                    '三': '3', '四': '4', '五' :'5',
                    '六': '6', '七': '7', '八': '8',
                    '九': '9', '十': '10', '丁目': '-'}

    # Use regular expressions to replace characters
    for k, v in convert_map.items():
        input_string = re.sub(k, v, input_string)

    return input_string


def full_norm(address):
    normalized_address = normalize(address)
    joined_address = normalized_address['pref'] + normalized_address['city'] + normalized_address['town'] + normalized_address['addr']
    addr = jaconv.z2h(joined_address, digit=True, ascii=False)
    addr = replace_address(addr)
    return addr