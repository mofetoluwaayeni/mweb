
                    MWEB DOCUMENTATION
                    Version 1.0.0


TABLE OF CONTENTS

1. Overview
2. Features
3. Installation
4. Usage Guide
5. Module Reference
6. Architecture
7. Configuration
8. Security Considerations
9. Sample Output
10. Troubleshooting
11. Development


1. OVERVIEW


MWEB (Modular Web Enumeration & Benchmarking) is a professional web 
reconnaissance framework designed for cybersecurity professionals, penetration 
testers, and security researchers.

The tool performs comprehensive automated reconnaissance against target domains,
collecting WHOIS data, DNS records, IP geolocation, HTTP headers, SSL/TLS 
certificates, and discovery files.

Key Design Principles:
- Modular architecture for extensibility
- Production-quality code with type hints
- Async I/O for performance
- Professional reporting (Markdown/HTML)
- Comprehensive error handling


2. FEATURES


CORE MODULES:
-------------
[+] WHOIS Module
    - Domain registration details
    - Registrar information
    - Creation/expiration dates
    - Name server enumeration
    - DNSSEC status

[+] DNS Module
    - Multiple record types (A, AAAA, MX, NS, TXT, CNAME, SOA, PTR, SRV, CAA)
    - Zone transfer detection (AXFR)
    - Reverse DNS lookups
    - Custom DNS server support

[+] IP Geolocation Module
    - IP address resolution (IPv4/IPv6)
    - Geographic location data
    - ASN and ISP information
    - CDN/cloud provider detection

[+] HTTP Module
    - Response header analysis
    - Security header assessment (CSP, HSTS, X-Frame-Options, etc.)
    - Technology fingerprinting
    - Redirect chain tracking

[+] SSL/TLS Module
    - Certificate chain validation
    - Cipher suite analysis
    - SSL version detection
    - Vulnerability detection (weak ciphers, expiration)

[+] Crawler Module
    - robots.txt parsing
    - sitemap.xml extraction
    - security.txt discovery
    - Exposed sensitive file detection

REPORTING:
----------
- Markdown reports with tables and code blocks
- HTML reports with CSS styling
- JSON output for programmatic use
- Risk scoring with recommendations


3. INSTALLATION


REQUIREMENTS:

- Python 3.12 or higher
- pip package manager
- Internet connection for reconnaissance

INSTALLATION STEPS:


1. Clone or extract the MWEB archive:

   $ git clone https://github.com/yourusername/mweb.git
   $ cd mweb

2. Create a virtual environment:

   $ python3.12 -m venv venv

3. Activate the virtual environment:

   Linux/Mac:
   $ source venv/bin/activate

   Windows:
   $ venv\Scripts\activate

4. Install dependencies:

   $ pip install -r requirements.txt

DEPENDENCIES (from requirements.txt):

dnspython>=2.4.0
requests>=2.31.0
python-whois>=0.8.0
geoip2>=4.7.0
cryptography>=41.0.0
beautifulsoup4>=4.12.0
jinja2>=3.1.0
click>=8.1.0
rich>=13.5.0
urllib3>=2.0.0


4. USAGE GUIDE


BASIC USAGE:


Scan a domain with all modules:
   $ python mweb.py example.com

Scan with verbose output:
   $ python mweb.py example.com -v

ADVANCED OPTIONS:


Select specific modules:
   $ python mweb.py example.com -m dns,ssl_tls,http

Generate HTML report:
   $ python mweb.py example.com -f html

Specify output directory:
   $ python mweb.py example.com -o ./my_reports

Combine options:
   $ python mweb.py example.com -m dns,http,ssl_tls -f html -o ./reports -v

AVAILABLE MODULES FOR -m FLAG:

whois       - WHOIS domain information
dns         - DNS record enumeration
ipgeo       - IP resolution and geolocation
http        - HTTP header analysis
ssl_tls     - SSL/TLS certificate analysis
crawler     - Discovery file crawling

OUTPUT FORMATS (-f FLAG):

markdown    - Markdown format (default)
html        - Styled HTML report
json        - Raw JSON data


5. MODULE REFERENCE


WHOIS MODULE:

Purpose: Retrieve domain registration information
Data Collected:
  - Registrar name
  - Creation/expiration/update dates
  - Name servers
  - Registrant contact info (if available)
  - DNSSEC status
  - Domain status codes

DNS MODULE:

Purpose: Enumerate DNS infrastructure
Data Collected:
  - A/AAAA records (IPv4/IPv6 addresses)
  - MX records (mail servers)
  - NS records (name servers)
  - TXT records (SPF, DKIM, verification)
  - CNAME records (aliases)
  - SOA records (zone authority)
  - Zone transfer vulnerability status
  - Reverse DNS mappings

IP GEOLOCATION MODULE:

Purpose: Locate and identify hosting infrastructure
Data Collected:
  - Resolved IP addresses
  - Geographic coordinates
  - City, region, country
  - ISP and organization
  - ASN information
  - Detected CDN/cloud providers

HTTP MODULE:

Purpose: Analyze web server configuration
Data Collected:
  - Response status codes
  - Server headers
  - Content-Type and encoding
  - Security headers (CSP, HSTS, etc.)
  - Technology stack fingerprinting
  - Redirect chains

Security Headers Checked:
  - Content-Security-Policy
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - X-XSS-Protection
  - Referrer-Policy
  - Permissions-Policy
  - Cross-Origin headers

SSL/TLS MODULE:

Purpose: Analyze certificate and encryption
Data Collected:
  - Certificate subject/issuer
  - Validity dates
  - Serial number
  - Subject Alternative Names (SAN)
  - SSL/TLS version
  - Cipher suite details
  - Key usage extensions
  - Vulnerability indicators

Vulnerabilities Detected:
  - Expired certificates
  - Weak cipher suites (RC4, DES, etc.)
  - Outdated TLS versions (< 1.2)
  - Missing certificate chain

CRAWLER MODULE:

Purpose: Discover configuration and sensitive files
Data Collected:
  - robots.txt content and rules
  - sitemap.xml URLs
  - security.txt contact info
  - Potentially exposed files

Files Checked:
  - /.env
  - /.git/config
  - /.htaccess
  - /config.php
  - /wp-config.php
  - /admin/
  - /api/
  - /swagger.json
  - /openapi.json


6. ARCHITECTURE


PROJECT STRUCTURE:


mweb/
├── mweb/
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Module entry point
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # Configuration management
│   ├── core/                    # Reconnaissance modules
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base class
│   │   ├── whois_module.py
│   │   ├── dns_module.py
│   │   ├── ipgeo_module.py
│   │   ├── http_module.py
│   │   ├── ssl_module.py
│   │   └── crawler_module.py
│   ├── reporters/               # Report generators
│   │   ├── __init__.py
│   │   ├── base.py              # Base reporter class
│   │   ├── markdown_reporter.py
│   │   └── html_reporter.py
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── logger.py              # Logging setup
│       └── validators.py          # Input validation
├── tests/
│   └── test_modules.py
├── requirements.txt
├── README.md
└── mweb.py                      # Main entry point

DESIGN PATTERNS:


1. Modular Architecture
   - Each reconnaissance module inherits from BaseModule
   - Standardized ModuleResult return type
   - Easy to extend with new modules

2. Async I/O
   - Uses asyncio for concurrent operations
   - Thread pools for blocking I/O (WHOIS, DNS)
   - Improves performance for multiple modules

3. Configuration Management
   - Dataclass-based config
   - Environment-specific settings
   - Sensible defaults

4. Reporting Strategy Pattern
   - BaseReporter defines interface
   - Multiple output formats
   - Consistent risk scoring


7. CONFIGURATION


CONFIGURATION OPTIONS (config.py):


HTTP Settings:
  timeout           - Request timeout in seconds (default: 30)
  user_agent        - HTTP User-Agent string
  follow_redirects  - Follow HTTP redirects (default: True)
  max_redirects     - Maximum redirect hops (default: 5)

SSL/TLS Settings:
  ssl_verify        - Verify SSL certificates (default: True)
  ssl_timeout       - SSL handshake timeout (default: 10)

DNS Settings:
  dns_servers       - List of DNS resolvers to use
  Default: ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

Rate Limiting:
  request_delay     - Delay between requests in seconds (default: 0.5)
  max_retries       - Maximum retry attempts (default: 3)

Security Headers:
  security_headers  - List of headers to check for

Crawler Paths:
  crawl_paths       - URLs to check for discovery files

CUSTOMIZING CONFIGURATION:


Edit mweb/config.py:

  from mweb.config import Config
  
  config = Config()
  config.timeout = 60
  config.dns_servers = ["8.8.8.8"]
  config.log_level = "DEBUG"


8. SECURITY CONSIDERATIONS


AUTHORIZED USE ONLY:


MWEB is designed for authorized security testing only. Always ensure you have:

1. Written authorization to test the target
2. Legal permission under applicable laws
3. Compliance with your organization's policies

RESPONSIBLE DISCLOSURE:


If you discover vulnerabilities:
1. Do not exploit them beyond verification
2. Report to the appropriate contact
3. Follow responsible disclosure practices
4. Allow reasonable time for remediation

RATE LIMITING:

Be respectful of target resources:
- Default 0.5 second delay between requests
- Adjust for target capacity
- Consider off-peak hours for large scans

PRIVACY CONSIDERATIONS:


- WHOIS data may contain personal information
- Store reports securely
- Comply with data protection regulations
- Encrypt sensitive findings


9. SAMPLE OUTPUT


CONSOLE OUTPUT:
-

🔒 MWEB Scanner
Target: example.com

✓ Report generated: reports/mweb_report_example.com_20250720_143022.md

┌─────────┬────────┬─────────┐
│ Module  │ Status │ Details │
├─────────┼────────┼─────────┤
│ whois   │ ✓      │ OK      │
│ dns     │ ✓      │ OK      │
│ ipgeo   │ ✓      │ OK      │
│ http    │ ✓      │ OK      │
│ ssl_tls │ ✓      │ OK      │
│ crawler │ ✓      │ OK      │
└─────────┴────────┴─────────┘

MARKDOWN REPORT EXCERPT

# MWEB Reconnaissance Report

**Target:** `example.com`  
**Generated:** 20250720_143022  
**Risk Score:** 72/100 (Fair)



## Executive Summary

This report contains findings from automated reconnaissance against 
**example.com**. The overall security posture is rated as **Fair**.

### Key Findings

- ⚠️ Missing header: Strict-Transport-Security
- ⚠️ Missing header: Content-Security-Policy
- ⚠️ SSL/TLS: Certificate expires in 45 days



## WHOIS Information

| Field | Value |
|-------|-------|
| Registrar | Example Registrar, LLC |
| Creation Date | 2020-01-15T00:00:00 |
| Expiration Date | 2025-01-15T00:00:00 |
| DNSSEC | unsigned |

**Name Servers:**
- ns1.example.com
- ns2.example.com

---

## DNS Records

### A Records
- `93.184.216.34`

### MX Records
- `10 mail.example.com`
- `20 mail2.example.com`

---

## Recommendations

1. **SSL/TLS Hardening:** Address certificate expiration
2. **Security Headers:** Implement HSTS and CSP headers
3. **DNS Security:** Consider enabling DNSSEC


10. TROUBLESHOOTING


COMMON ISSUES:
--------------

Issue: "Module failed: Connection timeout"
Solution: Increase timeout in config.py:
  config.timeout = 60

Issue: "DNS resolution failed"
Solution: Check DNS servers or network connectivity:
  - Verify internet connection
  - Try different DNS servers
  - Check firewall settings

Issue: "SSL certificate verify failed"
Solution: For testing only, disable verification:
  config.ssl_verify = False
  WARNING: This reduces security, use only for testing

Issue: "Permission denied writing report"
Solution: Check output directory permissions:
  $ chmod 755 reports/
  or specify different output directory

Issue: "ImportError: No module named X"
Solution: Install missing dependency:
  $ pip install -r requirements.txt

DEBUGGING:

Enable verbose mode:
  $ python mweb.py example.com -v

Enable debug logging in code:
  from mweb.utils.logger import setup_logger
  logger = setup_logger("mweb", "DEBUG")

Check module results:
  $ python mweb.py example.com -f json


11. DEVELOPMENT


RUNNING TESTS:


$ pytest tests/

TYPE CHECKING:


$ mypy mweb/

CODE FORMATTING:


$ black mweb/
$ flake8 mweb/

ADDING NEW MODULES:


1. Create module file in mweb/core/
2. Inherit from BaseModule
3. Implement run() method
4. Return ModuleResult
5. Register in MWEBScanner.modules

Example:

from mweb.core.base import BaseModule, ModuleResult

class MyModule(BaseModule):
    @property
    def module_name(self) -> str:
        return "my_module"
    
    async def run(self, target: str) -> ModuleResult:
        # Your implementation
        data = {"key": "value"}
        return self._create_result(success=True, data=data)

ADDING NEW REPORTERS:


1. Inherit from BaseReporter
2. Implement generate() method
3. Register in CLI


2

Copyright (c) 2024 MWEB Contributors



                         END OF DOCUMENTATION


For updates and support:
- GitHub: https://github.com/mofetoluwaayeni/mweb


Report bugs and feature requests via GitHub Issues
