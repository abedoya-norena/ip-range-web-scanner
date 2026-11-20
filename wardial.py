import requests


def is_server_at_hostname(hostname):
    '''
    Return True if an HTTP GET to the hostname (domain or IP) returns status 200.
    Uses a 5 s timeout so unreachable hosts don't stall the scan.

    >>> is_server_at_hostname('google.com')
    True
    >>> is_server_at_hostname('GoOgLe.CoM')
    True
    >>> is_server_at_hostname('google.commmm')
    False
    >>> is_server_at_hostname('142.250.68.110.1.3.4.5')
    False
    '''
    try:
        r = requests.get('http://' + hostname, timeout=5)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def increment_ip(ip):
    '''
    Return the "next" IPv4 address.

    >>> increment_ip('1.2.3.4')
    '1.2.3.5'
    >>> increment_ip('1.2.3.255')
    '1.2.4.0'
    >>> increment_ip('0.0.0.0')
    '0.0.0.1'
    >>> increment_ip('0.0.0.255')
    '0.0.1.0'
    >>> increment_ip('0.0.255.255')
    '0.1.0.0'
    >>> increment_ip('0.255.255.255')
    '1.0.0.0'
    >>> increment_ip('0.255.5.255')
    '0.255.6.0'
    >>> increment_ip('255.255.255.255')
    '0.0.0.0'
    '''

    split_parts = ip.split('.')

    parts = []
    for x in split_parts:
        parts.append(int(x))

    for i in range(3, -1, -1):

        if parts[i] < 255:
            parts[i] = parts[i] + 1
            break
        else:
            parts[i] = 0

    string_parts = []
    for x in parts:
        string_parts.append(str(x))

    result = '.'.join(string_parts)

    return result
        
    


def enumerate_ips(start_ip, n):
    '''
    Return a list containing the next `n` IPs beginning with `start_ip`.

    >>> list(enumerate_ips('192.168.1.0', 2))
    ['192.168.1.0', '192.168.1.1']

    >>> list(enumerate_ips('8.8.8.8', 10))
    ['8.8.8.8', '8.8.8.9', '8.8.8.10', '8.8.8.11', '8.8.8.12', '8.8.8.13', '8.8.8.14', '8.8.8.15', '8.8.8.16', '8.8.8.17']

    >>> list(enumerate_ips('192.168.0.255', 2))
    ['192.168.0.255', '192.168.1.0']

    >>> len(list(enumerate_ips('8.8.8.8', 10)))
    10
    >>> len(list(enumerate_ips('8.8.8.8', 1000)))
    1000
    >>> len(list(enumerate_ips('8.8.8.8', 100000)))
    100000
    '''
    ip = start_ip
    for _ in range(n):
        yield ip
        ip = increment_ip(ip)
    


if __name__ == '__main__':

    dprk_ips = list(enumerate_ips('175.45.176.0', 1024))

    dprk_ips_with_servers = []

    for ip in dprk_ips:
        print("Scanning:", ip)

        if is_server_at_hostname(ip):
            dprk_ips_with_servers.append(ip)

    print('dprk_ips_with_servers=', dprk_ips_with_servers)
