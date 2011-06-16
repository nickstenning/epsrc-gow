# coding=utf8

import re

_extract_id_memo = {}

def extract_id(str, type):
    pattern = _extract_id_memo.get(type)

    if not pattern:
        pattern = _extract_id_memo[type] = r"%sId=(\-?\d+)" % type

    m = re.search(pattern, str)
    return int(m.group(1))

def extract_monetary_value(str):
    return float(re.sub(r"[£,]", '', str))