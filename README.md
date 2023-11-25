# DomainDetective
![Group 9](https://github.com/as-squirrel/DomainDetective/assets/114065413/ae7437a3-73f0-4d0b-b270-a7edfd762e14)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/as-squirrel/DomainDetective)
![GitHub issues](https://img.shields.io/github/issues/as-squirrel/DomainDetective)
![GitHub pull requests](https://img.shields.io/github/issues-pr/as-squirrel/DomainDetective)
![GitHub stars](https://img.shields.io/github/stars/as-squirrel/DomainDetective)
![GitHub forks](https://img.shields.io/github/forks/as-squirrel/DomainDetective)

## Description
The Subdomain Checker tool allows users to verify the existence of subdomains belonging to a main domain and optionally check SSL certificates for these subdomains. The tool provides a comprehensive report in the form of a CSV file and visualizations to understand the distribution and trends of subdomains over time.

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
- Visualizations for understanding subdomain trends.


## Example
```bash
python main.py example.com subdomains.txt --ports 443 --timeout 10 --https --output found_subdomains.txt --check-certificates
```
### visualizations 

![Opera Momentaufnahme_2023-11-25_231337_127 0 0 1](https://github.com/as-squirrel/DomainDetective/assets/114065413/520ece2b-e8b6-4ec9-a327-0f07ff0f8a38)


# Notes
Usage of this tool without proper authorization may violate applicable laws.
Ensure the tool's usage aligns with ethical standards and laws in your region.
