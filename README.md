# NordVPN Tray

### A cross-platform system tray application for interacting with Nord VPN.

[![nordvpn-tray](https://github.com/aviolaris/nordvpn-tray/assets/48277853/cb21498f-a2fd-4fed-ab6e-3da6a8cd1f3d)](https://github.com/aviolaris/nordvpn-tray)

![python-versions](https://img.shields.io/pypi/pyversions/nordvpn-tray)
[![pypi-downloads](https://img.shields.io/pypi/dm/nordvpn-tray.svg?color=blue&label=downloads&logo=pypi&logoColor=gold)](https://pypistats.org/packages/nordvpn-tray)

[![license](https://img.shields.io/pypi/l/nordvpn-tray?color=blueviolet)](https://github.com/aviolaris/nordvpn-tray/blob/master/LICENSE)
![format](https://img.shields.io/pypi/format/nordvpn-tray?color=blueviolet)
![status](https://img.shields.io/pypi/status/nordvpn-tray?color=blue)
[![GitHub Stars](https://img.shields.io/github/stars/aviolaris/nordvpn-tray?color=blue&logo=github&logoColor=white)](https://github.com/aviolaris/nordvpn-tray/stargazers)

## Description

The official NordVPN clients for both Windows and Linux have well-known limitations. For instance, in Windows, to list
all servers of a specific country, you must use a search pattern like ```country_name #```, while in Linux, it is not
possible at all. Furthermore, regardless of the platform, these clients do not provide essential information such as the
server's load and external IP, even if the user has the corresponding identification code.

To overcome these limitations, the current project expands the functionality of the official clients by introducing a
solution in the form of a cross-platform system tray application. By placing an icon in the system tray, users can
easily access a menu displaying the complete list of available NordVPN servers. The servers are conveniently categorized
by continents and countries, allowing for effortless navigation. Moreover, they are ordered by their load, enabling
users to select the server with the lowest load for optimal performance.

## Preview

<img src="https://github.com/aviolaris/nordvpn-tray/assets/48277853/b4458286-efa2-4e0d-99e2-948d8df8aca8" alt="Preview" width="500">

## Requirements

- The official NordVPN client (available [here](https://nordvpn.com/download/))

## Installation

To install NordVPN Tray, run the following command:

    pip install nordvpn-tray

## Usage

To launch NordVPN Tray:

- **On Windows**, double-click the `nordvpn-tray.exe` (usually located
  in `%LOCALAPPDATA%\Programs\Python\Python##\Scripts`) or run the `nordvpn-tray` command from the command prompt.


- **On Linux**, double-click the `nordvpn-tray` (usually located in `~/.local/bin`) or run the `./nordvpn-tray` command
  from the terminal.

## Common Issues

#### "ValueError: Namespace AppIndicator3 not available" (Linux Only)

This error message indicates that the `AppIndicator3` module, which the application uses to display tray icons on Linux,
is not available on your system.

To resolve this issue, you will need to install the `libayatana-appindicator3-dev` package, which provides the necessary
files and libraries for the `AppIndicator3` module. To install the package, use the following command:

    sudo apt-get install libayatana-appindicator3-dev

## Disclaimer

All trademarks, logos and brand names are the property of their respective owners. All company and service names used in
this repository are for identification purposes only. The use of NordVPN trademarks does not imply any endorsement,
partnership, or sponsorship by Nordsec Ltd.

## Contribution

Pull requests and issues are welcome.

## License

This project is licensed under the GNU General Public License v3.0.

See the [LICENSE](https://github.com/aviolaris/nordvpn-tray/blob/master/LICENSE) file for details.