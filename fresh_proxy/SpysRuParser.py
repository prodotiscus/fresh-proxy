import requests
import re

# Spys.Ru Proxy List Parser

def getAllProxies():
    ps_prepare = requests.get('http://spys.ru/proxies').text
    xf_token = re.search(
        r"name='xf0'\svalue='[a-f\d]+", ps_prepare
    ).group(0).split("'")[3]
    proxy_code = requests.post(
        'http://spys.ru/proxies/',
        {
            'xpp' : 4,
            'xf1' : 0,
            'xf0' : xf_token,
            'xf2' : 0,
            'xf4' : 0
        }
    ).text
    odf_declaration = re.search(
        r'([a-z\d]+=[\^a-z\d]+;)+', proxy_code.split('</script>')[3]
    ).group(0)[:-1]
    for declaration in odf_declaration.split(';'):
        exec(declaration)
    found_ips = re.findall(
        r'<font\sclass=spy14>[^A-Z<]+<script\stype=\"text\/javascript\">' +
        '[^<]+<font\sclass=spy2>:<\\\/font>"\+[a-z\^\d\(\)\+]+',
        proxy_code
    )
    selected_ips = []
    for fi in found_ips:
        fi_parts = fi.split(
            '<script type="text/javascript">' +
            'document.write("<font class=spy2>:<\\/font>"+'
        )
        ip_addr = fi_parts[0][18:]
        ip_port = ''
        for splitted_expr in fi_parts[1][:-1].split('+'):
            ip_port += str(eval(splitted_expr))
        selected_ips.append(ip_addr + ':' + ip_port)
    return selected_ips