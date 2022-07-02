from sheets.int_to_col import int_to_col
from sheets.read import get_values
from sheets.write import update_value

def add_mark(spreadsheet_id: str, assesment: str, std_id: int, mark: int) -> str :
  try:
    id = str(std_id)
    all_ass = get_values(spreadsheet_id,"1:1")[0][1::]
    if (all_ass.count(assesment) == 0):
      return "Error: Assesment Doesn't Exists!"
    all_std_2d = get_values(spreadsheet_id,"A:A")
    all_std = []
    for index, element in enumerate(all_std_2d):
      if index != 0:
        if len(element) == 0:
          all_std.append("")
        else:
          all_std.append(element[0])
    if(all_std.count(id) == 0):
      return "Error: Student Doesn't Exists!"
    range_col = int_to_col(all_ass.index(assesment)+2)
    range_row = str(all_std.index(id)+2)
    range = range_col+range_row
    update_value(spreadsheet_id,range+":"+range,mark)
    return ""
  except Exception as e:
    return repr(e)

# print(add_mark("1YW-xAqLd4Bc-ImFkCql81ZsA4Zp6xKHOM3Y9uedDv6E","Test 1", 5, 5))