import string
# 1 based
def int_to_col(n: int,b=string.ascii_uppercase) -> str:
  n -= 1
  d, m = divmod(n,len(b))
  return int_to_col(d-1,b)+b[m] if d else b[m]