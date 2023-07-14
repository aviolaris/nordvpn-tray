"""
NordVPN Tray - A cross-platform system tray application for interacting with Nord VPN.
Copyright (C) 2023 Andreas Violaris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import os
import re
import subprocess
from country_converter import CountryConverter
from PIL import Image
import pkg_resources
import pystray
from pystray import Icon
import requests


def get_full_domain_identifier(short_domain_identifier):
    country_converter = CountryConverter()
    country_code = short_domain_identifier[:2].upper()
    country_name = country_converter.convert(names=country_code, to='name_short')
    if country_name:
        return f"{country_name} #{short_domain_identifier[2:]}"
    else:
        return "Invalid country code"


def is_nordvpn_connected():
    user_info_data = requests.get(
        b'\x68\x74\x74\x70\x73\x3a\x2f\x2f\x6e\x6f\x72\x64\x76\x70\x6e\x2e\x63\x6f'
        b'\x6d\x2f\x77\x70\x2d\x61\x64\x6d\x69\x6e\x2f\x61\x64\x6d\x69\x6e\x2d\x61'
        b'\x6a\x61\x78\x2e\x70\x68\x70\x3f\x61\x63\x74\x69\x6f\x6e\x3d\x67\x65\x74'
        b'\x5f\x75\x73\x65\x72\x5f\x69\x6e\x66\x6f\x5f\x64\x61\x74\x61',
        timeout=10)
    if user_info_data.status_code == 200:
        data = user_info_data.json()
        return data.get('status', False)
    return False


def create_connect_callback(domain):
    def callback(icon, domain):
        domain_identifier = re.search(r"\[(\w+)\.nordvpn\.com]", str(domain)).group(1)
        full_domain_identifier = get_full_domain_identifier(domain_identifier)
        if domain_identifier:
            if is_nordvpn_connected():
                icon.notify("Already connected to a NordVPN server.")
            else:
                icon.notify(str(domain))
                if os.name == 'nt':
                    command = f'cd C:/Program Files/NordVpn/ & nordvpn -c -n "{full_domain_identifier}"'
                else:
                    command = f"nordvpn connect {full_domain_identifier}"
                subprocess.run(command, shell=True)

    return callback


def create_disconnect_callback():
    def callback(icon, item):
        if is_nordvpn_connected():
            icon.notify("Disconnecting...")
            if os.name == 'nt':
                command = 'cd C:/Program Files/NordVpn/ & nordvpn -d'
            else:
                command = 'nordvpn d'
            subprocess.run(command, shell=True)
        else:
            icon.notify("You are not connected to a NordVPN server.")

    return callback


def quit(icon, item):
    icon.stop()


def main():
    country_converter = CountryConverter()

    nord_api = requests.get(
        b'\x68\x74\x74\x70\x73\x3a\x2f\x2f\x61\x70\x69\x2e\x6e\x6f\x72'
        b'\x64\x76\x70\x6e\x2e\x63\x6f\x6d\x2f\x73\x65\x72\x76\x65\x72',
        timeout=10)

    if nord_api.status_code == 200:
        servers = nord_api.json()
        countries_dict = {}
        for server in servers:
            country = server['country']
            flag = server['flag']
            domain = server['domain']
            ip_address = server['ip_address']
            load = server['load']
            if country == 'United States':
                if 'United States' in countries_dict and len(countries_dict['United States']) < 1100:
                    countries_dict['United States'].append((domain, ip_address, load, flag))
                elif 'United States' not in countries_dict:
                    countries_dict['United States'] = [(domain, ip_address, load, flag)]
            else:
                if country in countries_dict:
                    countries_dict[country].append((domain, ip_address, load, flag))
                else:
                    countries_dict[country] = [(domain, ip_address, load, flag)]
    else:
        print(f"Failed to fetch data, status code: {nord_api.status_code}")

    continent_dict = {}
    for country, domains_loads in sorted(countries_dict.items()):
        domain_items = []
        for domain_load in sorted(domains_loads, key=lambda x: x[2]):
            domain, ip_address, load, flag = domain_load
            subitem = pystray.MenuItem(f"[{str(load).zfill(2)}] [{domain}] [{ip_address}]",
                                       create_connect_callback(domain))
            domain_items.append(subitem)
        submenu = pystray.Menu(*domain_items)
        continent = country_converter.convert(names=country, to='continent')
        if continent in continent_dict:
            continent_dict[continent].append((country, submenu, flag))
        else:
            continent_dict[continent] = [(country, submenu, flag)]

    menu_items = []
    for continent, country_submenus_flags in sorted(continent_dict.items()):
        country_items = []
        for country_submenu_flag in sorted(country_submenus_flags):
            country, submenu, flag = country_submenu_flag
            country_item = pystray.MenuItem(f"{country} ({flag})", submenu)
            country_items.append(country_item)
        continent_menu = pystray.Menu(*country_items)
        menu_items.append(pystray.MenuItem(continent, continent_menu))

    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem("Disconnect", create_disconnect_callback()))
    menu_items.append(pystray.MenuItem("Quit", quit))

    menu = pystray.Menu(*menu_items)

    tray = Icon("NordVPN Tray")
    tray.icon = Image.open(pkg_resources.resource_filename(__name__, 'resources/nvt.ico'))
    tray.title = "NordVPN Tray"
    tray.menu = menu
    tray.run()


if __name__ == '__main__':
    main()
