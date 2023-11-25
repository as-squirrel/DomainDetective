import csv
import requests
import ssl
import time
import OpenSSL.crypto as crypto
from colorama import Fore, Style
import argparse
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots  

def check_subdomain(subdomain, main_domain, ports, timeout, use_https, output_file, check_certificates, user_agent):
    headers = {'User-Agent': user_agent} if user_agent else {}
    csv_columns = ['Timestamp', 'Subdomain', 'Domain', 'Port', 'Status Code', 'Time Taken']

    for port in ports:
        url = f"http://{subdomain}.{main_domain}:{port}" if not use_https else f"https://{subdomain}.{main_domain}:{port}"
        try:
            start_time = time.time()  # Capture start time of the request
            response = requests.get(url, timeout=timeout, headers=headers)
            end_time = time.time()  # Capture end time of the request
            response.raise_for_status()
            if response.status_code == 200:
                data = {
                    'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Subdomain': subdomain,
                    'Domain': main_domain,
                    'Port': port,
                    'Status Code': response.status_code,
                    'Time Taken': f"{end_time - start_time:.2f} seconds"
                }                
                print(f"{Fore.GREEN}Subdomain found: {subdomain}.{main_domain} on Port {port}{Style.RESET_ALL}")
                if output_file:
                    with open(output_file, mode='a', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=csv_columns)
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(data)
                if check_certificates:
                    cert = ssl.get_server_certificate((f"{subdomain}.{main_domain}", port))
                    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
                    print(f"{Fore.BLUE}SSL Certificate for {subdomain}.{main_domain} (Port {port}):{Style.RESET_ALL}\n")
                    print(f"Issuer: {x509.get_issuer()}")
                    print(f"Subject: {x509.get_subject()}")
                    print(f"Expiration Date: {x509.get_notAfter().decode('utf-8')}")

                log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Checked {subdomain}.{main_domain} on Port {port}\n"
                if output_file:
                    with open(output_file, "a") as file:
                        file.write(log_entry)
                    print(log_entry.strip())

        except requests.ConnectionError as ce:
            pass

        except requests.Timeout as te:
            error_msg = f"{Fore.RED}Error while checking {subdomain}.{main_domain}: Timeout Error - {te}{Style.RESET_ALL}\n"
            log_error(error_msg, output_file)

        except requests.HTTPError as he:
            error_msg = f"{Fore.RED}Error while checking {subdomain}.{main_domain}: HTTP Error - {he}{Style.RESET_ALL}\n"
            log_error(error_msg, output_file)

        except requests.RequestException as e:
            if "NewConnectionError" in str(e):
                error_msg = f"{Fore.RED}Error while checking {subdomain}.{main_domain}: Connection Error - Failed to establish a connection{Style.RESET_ALL}\n"
            else:
                error_msg = f"{Fore.RED}Error while checking {subdomain}.{main_domain}: {e}{Style.RESET_ALL}\n"
            log_error(error_msg, output_file)

        except Exception as e:
            error_msg = f"{Fore.RED}Error while checking {subdomain}.{main_domain}: {e}{Style.RESET_ALL}\n"
            log_error(error_msg, output_file)

def visualize_results(results_file):
    df = pd.read_csv(results_file, parse_dates=['Timestamp'])

    fig_line = px.line(df, x="Timestamp", y="Time Taken", color="Subdomain", line_group="Subdomain",
                       labels={"Time Taken": "Time Taken (seconds)", "Timestamp": "Timestamp"},
                       title="Time Taken for Different Subdomains Over Time")
    fig_line.update_layout(xaxis_title="Timestamp", yaxis_title="Time Taken (seconds)")

    fig_box = px.box(df, x="Subdomain", y="Time Taken",
                     labels={"Time Taken": "Time Taken (seconds)", "Subdomain": "Subdomain"},
                     title="Distribution of Time Taken Across Subdomains")
    fig_box.update_layout(xaxis_title="Subdomain", yaxis_title="Time Taken (seconds)")

    fig_hist = px.histogram(df, x="Time Taken",
                            labels={"Time Taken": "Time Taken (seconds)"},
                            title="Distribution of Time Taken")

    fig_bar = px.bar(df, x="Subdomain", y="Time Taken",
                     labels={"Time Taken": "Time Taken (seconds)", "Subdomain": "Subdomain"},
                     title="Time Taken Across Subdomains")

    fig_combined = make_subplots(rows=4, cols=1, subplot_titles=("Time Taken Over Time", "Time Taken Distribution Across Subdomains", "Time Taken Distribution", "Time Taken Across Subdomains"))

    for trace in fig_line.data:
        fig_combined.add_trace(trace, row=1, col=1)

    for trace in fig_box.data:
        fig_combined.add_trace(trace, row=2, col=1)

    for trace in fig_hist.data:
        fig_combined.add_trace(trace, row=3, col=1)

    for trace in fig_bar.data:
        fig_combined.add_trace(trace, row=4, col=1)

    fig_combined.update_layout(height=1200, showlegend=False)
    fig_combined.show()


def log_error(error_msg, output_file):
    log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}"
    print(log_entry.strip())
    if output_file:
        with open(output_file, "a") as file:
            file.write(log_entry)

def main():
    parser = argparse.ArgumentParser(description='Check subdomains for existence and SSL certificates')
    parser.add_argument('domain', help='Main domain to check against')
    parser.add_argument('file', help='File containing subdomains, one per line')
    parser.add_argument('--ports', nargs='+', default=[80, 443], type=int, help='Ports to check (default: 80, 443)')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout for each request in seconds (default: 5)')
    parser.add_argument('--https', action='store_true', help='Use HTTPS for checking')
    parser.add_argument('--output', default='results.csv', help='Output CSV file to store found subdomains')
    parser.add_argument('--check-certificates', action='store_true', help='Check SSL certificates for found subdomains')
    parser.add_argument('--user-agent', help='Custom User-Agent header for HTTP requests')
    args = parser.parse_args()

    main_domain = args.domain

    with open(args.file, "r") as file:
        subdomains = file.read().splitlines()


    for subdomain in subdomains:
        check_subdomain(subdomain, main_domain, args.ports, args.timeout, args.https, args.output, args.check_certificates, args.user_agent)
    


if __name__ == "__main__":
    main()
    visualize_results("results.csv")

