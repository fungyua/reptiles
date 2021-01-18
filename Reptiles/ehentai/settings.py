abs_path = "/Volumes/MacExt/reptiles/Reptiles/ehentai"
current_path = "/Volumes/MacExt/reptiles/Reptiles/ehentai"
aria2url = "http://127.0.0.1:16800/jsonrpc"
aria2token = "GJmTxqRCy4kS"
request_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
cookie_raw_ehentai = "ipb_member_id=4655141; ipb_pass_hash=9991257946307a4cc63e7fcf61dc7e6d; ipb_session_id=29dd586f9a83d4390e87d3b9bd528249; sk=sc46g3bq6tg65p8nsxaqgtjyue3w"
cookie_raw_exhentai = ''
proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}


def cookie_to_dict(cookie):
    item_dict = {}
    items = cookie.split(';')
    for item in items:
        tmp = item.split('=')
        key = tmp[0].replace(' ', '')
        value = tmp[1]
        item_dict[key] = value
    return item_dict


def cookie_ehentai(address):
    if "e-hentai" in address:
        return cookie_to_dict(cookie_raw_ehentai)
    elif "exhentai" in address:
        return cookie_to_dict(cookie_raw_exhentai)
    else:
        return cookie_to_dict(cookie_raw_ehentai)
