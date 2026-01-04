API Recon & Web Security Suite
Professional Web Reconnaissance & Security Assessment Tool

OVERVIEW

API Recon & Web Security Suite is a lightweight yet powerful Python-based web reconnaissance and security assessment tool designed for bug bounty hunters, security researchers, security consultants, and internal security teams. The tool focuses on high-signal, low-noise reconnaissance by automating common manual security checks that professionals perform during early-stage assessments.

The tool does not attempt exploitation. Instead, it helps identify exposed APIs, misconfigured endpoints, missing security headers, and sensitive paths that may lead to real vulnerabilities when manually validated. This makes it suitable for responsible disclosure programs, internal audits, and authorized penetration testing engagements.

PHILOSOPHY

Modern security teams prefer clarity over noise. This tool is designed to reduce false positives and highlight only meaningful findings. Each result is classified using severity labels to help users prioritize manual verification and reporting.

Severity Levels:
INFO      – Informational recon findings
POTENTIAL – Requires manual validation, often leads to real issues
HIGH      – Frequently reportable if confirmed

This severity-based approach mirrors how enterprise security tools and internal company scripts operate.

FEATURES

1. API RECONNAISSANCE SCAN

This module scans for commonly exposed API endpoints such as REST APIs, versioned APIs, Swagger/OpenAPI documentation, actuator endpoints, and administrative APIs. These endpoints are often unintentionally exposed in production environments and can lead to serious security issues.

Exposed API endpoints are flagged as POTENTIAL findings to encourage responsible manual validation before reporting or exploitation.

2. ENDPOINT HEALTH & AVAILABILITY CHECK

This module performs a basic health check against the target application, measuring HTTP response codes and response times. It provides quick visibility into endpoint availability and stability.

This is useful for internal security reviews, DevOps audits, and identifying backend instability that may indicate misconfiguration or denial-of-service weaknesses.

3. SECURITY HEADER ANALYSIS

The tool checks for commonly recommended HTTP security headers including:
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- Referrer-Policy

Missing headers are reported as informational findings, commonly used in compliance audits, security hardening reports, and low-to-medium severity bug bounty submissions.

4. ROBOTS.TXT PARSING & HIDDEN PATH DISCOVERY

This module retrieves the robots.txt file, extracts Disallow rules, and automatically tests the listed paths. It also scans for commonly sensitive paths such as:
- /.git
- /.env
- /admin
- /backup

While robots.txt itself is not a vulnerability, accessible disallowed paths are flagged as POTENTIAL or HIGH severity findings depending on response behavior.

USAGE

Interactive Mode:
python3 api_recon_suite.py

Direct Mode:
python3 api_recon_suite.py -u https://target.com

The tool automatically installs required dependencies on first run, making setup simple and user-friendly.

DEPENDENCIES

The tool automatically installs:
- requests
- colorama

No manual dependency installation is required.

TARGET USERS

- Bug bounty hunters seeking clean reconnaissance
- Security consultants performing authorized assessments
- Internal security teams building lightweight tooling
- Developers auditing their own applications
- Students transitioning into professional security work

DISCLAIMER

This tool is intended for educational and authorized security testing purposes only. Users are responsible for ensuring they have explicit permission before scanning any target system.

MONETIZATION & DISTRIBUTION

This tool can be sold or distributed as:
- A paid source tool via Gumroad, Ko-fi, or Buy Me a Coffee
- A portfolio project for freelance or full-time security roles
- An open-source tool with paid support or custom modules

The tool is suitable for ethical commercialization and professional use.

SUMMARY

This project demonstrates practical security engineering skills including:
- Automated reconnaissance logic
- Severity-based result classification
- Real-world web security checks
- Clean terminal UI
- Responsible disclosure mindset

This is not a toy script. It reflects real security workflows used by professionals.
