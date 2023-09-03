import re
from datetime import datetime


# e.g. date_string = '2022年09月28日11:23' => 2022-09-28T11:23:00

def from_jp_time(date_string):
    print(f"~~~~~~~~~~~~~~~{date_string}~~~~~~~~~~~~~~~~~~~~~~~~")
    match = re.match(r'(\d{4})年(\d{2})月(\d{2})日(\d{2}):(\d{2})', date_string)
    if match:
        year, month, day, hour, minute = map(int, match.groups())
        dt = datetime(year, month, day, hour, minute)
        print(f"~~~~~~~~~~~~~~~{dt}~~~~~~~~~~~~~~~~~~~~~~~~")
        return dt
    else:
        # 入力が期待する形式でない場合にはNoneを返す
        return None