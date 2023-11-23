# DomainDetective
![Group 9](https://github.com/as-squirrel/DomainDetective/assets/114065413/ae7437a3-73f0-4d0b-b270-a7edfd762e14)

## Description
The Subdomain Checker tool allows users to verify the existence of subdomains belonging to a main domain and optionally check SSL certificates for these subdomains.

## Installation
1. Make sure Python is installed.
2. Install required libraries:
    ```bash
    pip install -r requirements.txt

    ```

## Usage
```bash
python main.py domain file.txt [--ports PORTS] [--timeout TIMEOUT] [--https] [--output OUTPUT_FILE] [--check-certificates]
```

## Arguments
- `domain`: Main domain to check for subdomains.
- `file.txt`: File containing the list of subdomains to check.
- `--ports PORTS`: Specify ports for checking (default: 80, 443).
- `--timeout TIMEOUT`: Timeout for each request in seconds (default: 5).
- `--https`: Use HTTPS for checking.
- `--output OUTPUT_FILE`: Output file to save found subdomains.
- `--check-certificates`: Check SSL certificates for discovered subdomains.

## Features
- Verification of subdomain existence.
- Optional SSL certificate verification for discovered subdomains.
- Customizable ports, timeout, and output file.

## Example
```bash
python main.py example.com subdomains.txt --ports 443 --timeout 10 --https --output found_subdomains.txt --check-certificates
```

# Notes
Usage of this tool without proper authorization may violate applicable laws.
Ensure the tool's usage aligns with ethical standards and laws in your region.
