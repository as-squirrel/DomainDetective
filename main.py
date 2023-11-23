import argparse
import requests
import ssl
import time
import OpenSSL.crypto as crypto
from colorama import Fore, Style

def check_subdomain(subdomain, main_domain, ports, timeout, use_https, output_file, check_certificates):
    for port in ports:
        url = f"http://{subdomain}.{main_domain}:{port}" if not use_https else f"https://{subdomain}.{main_domain}:{port}"
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"{Fore.GREEN}Subdomain found: {subdomain}.{main_domain} on Port {port}{Style.RESET_ALL}")
                if output_file:
                    with open(output_file, "a") as file:
                        file.write(f"{subdomain}.{main_domain}:{port}\n")
                if check_certificates:
                    cert = ssl.get_server_certificate((f"{subdomain}.{main_domain}", port))
                    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
                    print(f"{Fore.BLUE}SSL Certificate for {subdomain}.{main_domain} (Port {port}):{Style.RESET_ALL}\n")
                    print(f"Issuer: {x509.get_issuer()}")
                    print(f"Subject: {x509.get_subject()}")
                    print(f"Expiration Date: {x509.get_notAfter().decode('utf-8')}")
        except requests.ConnectionError as ce:
            if not ("getaddrinfo failed" in str(ce) or "Invalid label" in str(ce)):
                print(f"{Fore.RED}Error while checking {subdomain}.{main_domain}: Connection Error - {ce}{Style.RESET_ALL}")
        except requests.Timeout as te:
            print(f"{Fore.RED}Error while checking {subdomain}.{main_domain}: Timeout Error - {te}{Style.RESET_ALL}")
        except requests.HTTPError as he:
            print(f"{Fore.RED}Error while checking {subdomain}.{main_domain}: HTTP Error - {he}{Style.RESET_ALL}")
        except requests.RequestException as re:
            print(f"{Fore.RED}Error while checking {subdomain}.{main_domain}: Request Exception - {re}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error while checking {subdomain}.{main_domain}: {e}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='Check subdomains for existence and SSL certificates')
    parser.add_argument('domain', help='Main domain to check against')
    parser.add_argument('file', help='File containing subdomains, one per line')
    parser.add_argument('--ports', nargs='+', default=[80, 443], type=int, help='Ports to check (default: 80, 443)')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout for each request in seconds (default: 5)')
    parser.add_argument('--https', action='store_true', help='Use HTTPS for checking')
    parser.add_argument('--output', help='Output file to store found subdomains')
    parser.add_argument('--check-certificates', action='store_true', help='Check SSL certificates for found subdomains')
    args = parser.parse_args()

    main_domain = args.domain

    with open(args.file, "r") as file:
        subdomains = file.read().splitlines()

    for subdomain in subdomains:
        check_subdomain(subdomain, main_domain, args.ports, args.timeout, args.https, args.output, args.check_certificates)

if __name__ == "__main__":
    main()
