# IP Range Web Scanner

![Tests](https://github.com/abedoya-norena/ip-range-web-scanner/actions/workflows/python-tests.yml/badge.svg)

Scans a block of IPv4 addresses and reports which ones host a live web server (HTTP 200).
Run here on the 1,024 addresses allocated to North Korea (175.45.176.0 – 175.45.179.255).

## How it works
- `increment_ip` / `enumerate_ips`: generate consecutive IPv4 addresses, with correct rollover across octets
- `is_server_at_hostname`: sends an HTTP GET with a 5 s timeout and returns True on a 200 response
- The main script walks the whole range and collects the responsive hosts

All functions have doctests, run automatically with GitHub Actions.

## Usage
```
$ python3 wardial.py
```

## Results
6 of 1,024 addresses responded with HTTP 200:
```
175.45.176.68
175.45.176.75
175.45.176.76
175.45.177.1
175.45.177.10
175.45.177.11
```

## Possible extensions
Scanning is sequential (~85 min worst case). A parallel version using `concurrent.futures` would finish in seconds.
