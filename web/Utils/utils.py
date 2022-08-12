

def get_sheet_id(url):
    res = url.split("/")
    return res[5]