import requests
import os
import argparse
import colorama
import subprocess
import platform
import random
from colorama import Fore, Style
from tqdm import tqdm

# Initialize colorama
colorama.init(autoreset=True)

# Check the OS
if platform.system() == 'Windows':
    hosts_file_path = r"c:\windows\system32\drivers\etc\hosts"
    dns_flush_command = 'ipconfig /flushdns'
elif platform.system() in ['Linux', 'Darwin']:  # Darwin = Mac
    hosts_file_path = '/etc/hosts'
    dns_flush_command = 'sudo killall -HUP mDNSResponder'
else:
    print(Fore.RED + 'Unsupported operating system.')
    exit(1)

# Create the parser
parser = argparse.ArgumentParser(
    description='Attempt to find the real IP address of a domain by brute forcing a list of IPs and checking the status code returned by the server.',
    usage='%(prog)s domain ipfile [-h] [--trace] [--cleandns] [--useragents uafile] [--timeout seconds] [--aggressive]',
    epilog='Examples:\n'
           '  %(prog)s www.example.com ip_addresses.txt\n'
           '  %(prog)s www.example.com ip_addresses.txt --trace --cleandns --useragents user_agents.txt --timeout 10 --aggressive\n',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# Add the arguments
parser.add_argument('Domain', metavar='domain', type=str, help='the domain to test')
parser.add_argument('IP_File', metavar='ipfile', type=str, help='the file containing the list of IP addresses')
parser.add_argument('--trace', dest='trace', action='store_true', help='activate trace file')
parser.add_argument('--cleandns', dest='cleandns', action='store_true', help='clean DNS cache after every hosts file change')
parser.add_argument('--useragents', metavar='uafile', type=str, help='the file containing the list of user agents')
parser.add_argument('--timeout', metavar='seconds', type=int, default=5, help='the timeout for each request in seconds')
parser.add_argument('--aggressive', dest='aggressive', action='store_true', help='perform more intensive checks')

# Parse the arguments
args = parser.parse_args()

domain = args.Domain
ip_file = args.IP_File
trace = args.trace
cleandns = args.cleandns
ua_file = args.useragents
timeout = args.timeout
aggressive = args.aggressive

if trace:
    trace_file = open('trace.txt', 'w')

try:
    with open(ip_file, 'r') as f:
        ip_addresses = f.readlines()
except FileNotFoundError:
    print(Fore.RED + f'File {ip_file} not found.')
    exit(1)

if ua_file:
    try:
        with open(ua_file, 'r') as f:
            user_agents = f.readlines()
    except FileNotFoundError:
        print(Fore.RED + f'User agent file {ua_file} not found.')
        exit(1)
else:
    user_agents = [None]

possible_ips = []

def check_url(ip, url):
    global possible_ips
    try:
        headers = {'User-Agent': ua} if ua else None
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            possible_ips.append(ip)
            print(Fore.GREEN + f'Real IP of the website might be: {ip}')
            if trace:
                trace_file.write(f'Real IP of the website might be: {ip}\n')
        elif r.status_code in [301, 302]:
            print(Fore.YELLOW + f'IP {ip} caused a redirect, might be real.')
            if trace:
                trace_file.write(f'IP {ip} caused a redirect, might be real.\n')
    except requests.exceptions.RequestException as err:
        if isinstance(err, requests.exceptions.ConnectTimeout):
            if trace:
                trace_file.write(f'Request for IP {ip} failed with timeout error: {err}\n')
        else:
            if trace:
                trace_file.write(f'Request for IP {ip} failed with error: {err}\n')

for ip in tqdm(ip_addresses, ncols=75, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
    ip = ip.strip()
    ua = random.choice(user_agents).strip() if user_agents[0] else None

    # Remove previous entries for the domain
    with open(hosts_file_path, 'r') as f:
        lines = f.readlines()

    with open(hosts_file_path, 'w') as f:
        for line in lines:
            if domain not in line:
                f.write(line)

    # Add new entry
    with open(hosts_file_path, 'a') as f:
        f.write(f'{ip} {domain}\n')

    if cleandns:
        os.system(dns_flush_command)

    # Check default and /404 pages for both HTTP and HTTPS
    for protocol in ['http', 'https']:
        check_url(ip, f'{protocol}://{domain}')
        if ip in possible_ips:
            break
        check_url(ip, f'{protocol}://{domain}/404')
        if ip in possible_ips:
            break

    # Aggressive mode checks
    if aggressive and ip not in possible_ips:
        for protocol in ['http', 'https']:
            for path in ['/robots.txt', '/license.txt', '/README.md']:
                check_url(ip, f'{protocol}://{domain}{path}')
                if ip in possible_ips:
                    break
            if ip in possible_ips:
                break

# Clean up after all attempts
with open(hosts_file_path, 'w') as f:
    for line in lines:
        if domain not in line:
            f.write(line)

if not possible_ips:
    print(Fore.RED + 'The IP could not be found.')
else:
    print(Fore.CYAN + 'Possible IP addresses found:')
    for ip in possible_ips:
        print(Fore.CYAN + ip)
if trace:
    trace_file.close()
