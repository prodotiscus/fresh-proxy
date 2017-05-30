#!/usr/bin/python3

import re
import requests

# HideMy.Name Proxy List Parser

def getAllProxies():
    hdr = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.114 Safari/537.36 Vivaldi/1.10.845.3'
    }
    ps_prepare = requests.get(
        'https://hidemy.name/ru/proxy-list/',
        headers = hdr
    ).text
    last_url = re.search(
        r'/ru/proxy-list/\?start=\d+#list(?=\">\d+</a></li></ul>)',
        ps_prepare
    ).group(0)
    last_url_index = int(re.search('\d+', last_url).group(0))
    selected_ips = []
    parsed_text = ps_prepare
    while len(selected_ips) < last_url_index:
        found_ips = re.findall(
            r'<td\sclass=tdl>\d+\.\d+\.\d+\.\d+<\/td><td>\d+</td><td><div>' +
            r'<span\sclass=\"flag-icon\sflag-icon-\w+\"></span>\s*&nbsp;[^<]+<span>[^<]+',
            parsed_text
        )
        for fi in found_ips:
            ip_object = {}
            ip_object['country'] = re.search('(?<=&nbsp;)(\w+\s*)+', fi).group(0)
            end_match = re.search('(?<=<span>).+$', fi).group(0)
            if not re.search('\w', end_match):
                ip_object['city'] = False
            else:
                ip_object['city'] = re.sub('^\s+|\s+$', '', end_match)
            single_ip = re.search('(?<=<td\sclass=tdl>)\d+\.\d+\.\d+\.\d+', fi).group(0)
            single_port = re.search(
                '<td\sclass=tdl>\d+\.\d+\.\d+\.\d+</td><td>(\d+)',
                fi
            ).group(1)
            ip_object['addr'] = single_ip + ':' + single_port
            selected_ips.append(ip_object)
        parsed_text = requests.get(
            'https://hidemy.name/ru/proxy-list/?start=' + str(len(selected_ips)) + '#list',
            headers = hdr
        ).text
    return selected_ips