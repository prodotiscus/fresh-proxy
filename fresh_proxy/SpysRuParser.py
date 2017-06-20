#!/usr/bin/python3

import requests
import re
import time

# Spys.Ru Proxy List Parser

def getSectionProxies(url, addr_only = False):
    ps_prepare = requests.get(url).text
    xf_token = re.search(
        r"name='xf0'\svalue='[a-f\d]+", ps_prepare
    ).group(0).split("'")[3]
    proxy_code = requests.post(
        url,
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
        r'[^<]+<font\sclass=spy2>:<\\\/font>"\+[a-z\^\d\(\)\+]+',
        proxy_code
    )
    found_locations = []
    for srch in re.finditer(
        '<font\sclass=spy14>[A-Z]{2}(\s<font\sclass=spy1>[^<]+<\/font>)*',
        proxy_code
    ):
        found_locations.append(srch.group(0))
    selected_ips = []
    for j in range(len(found_ips)):
        fi_parts = found_ips[j].split(
            '<script type="text/javascript">' +
            'document.write("<font class=spy2>:<\\/font>"+'
        )
        fi_location = found_locations[j]
        ip_object = {
            'addr' : '',
            'country' : '',
            'city' : False
        }
        if 'font class=spy1' in fi_location:
            ip_object['city'] = fi_location[38:-7]
        ip_object['country'] = fi_location[18:20]
        ip_addr = fi_parts[0][18:]
        ip_port = ''
        for splitted_expr in fi_parts[1][:-1].split('+'):
            ip_port += str(eval(splitted_expr))
        ip_object['addr'] = ip_addr + ':' + ip_port
        selected_ips.append(ip_object if not addr_only else ip_object['addr'])
    return selected_ips
def getAllProxies(countries = 20, addr_only = False, printing = False):
    if printing:
        print('Connecting to the recent proxies page...')
    base = getSectionProxies('http://spys.ru/proxies/', addr_only)
    if printing:
        print('Getting the proxy countries list...')
    pc_prepare = requests.get('http://spys.ru/proxys/').text
    proxy_countries = re.findall(r'\/proxys\/\w{2,4}\/', pc_prepare)
    if countries > len(proxy_countries):
        countries = len(proxy_countries)
    for i in range(countries):
        if printing:
            print('Connecting to ' + proxy_countries[i])
        base += getSectionProxies('http://spys.ru' + proxy_countries[i], addr_only)
        time.sleep(0.3)
    return base
