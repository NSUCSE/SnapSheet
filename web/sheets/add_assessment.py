from sheets.int_to_col import int_to_col
from sheets.read import get_values
from sheets.write import update_value

def add_assessment(spreadsheet_id: str, assesment: str) -> str :
  try:
    all_ass = get_values(spreadsheet_id,"1:1")[0][1::]
    if (all_ass.count(assesment) != 0):
      return "Error: Assesment Exists!"
    range = int_to_col(len(all_ass)+2)
    update_value(spreadsheet_id,range+":"+range,assesment)
    return ""
  except Exception as e:
    return repr(e)

# print(add_assessment("1YW-xAqLd4Bc-ImFkCql81ZsA4Zp6xKHOM3Y9uedDv6E","Test 5"))