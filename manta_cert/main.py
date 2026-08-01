"""SSL/TLS certificate checker — inspect expiry, issuer, and SANs."""

import argparse
import datetime
import ssl
import socket
import sys
from typing import List, Optional


def get_cert_info(host: str, port: int = 443, timeout: int = 10) -> dict:
    """Retrieve SSL/TLS certificate info for a host."""
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
    if not cert:
        print(f"error: no certificate returned for {host}:{port}", file=sys.stderr)
        sys.exit(1)
    return cert


def format_date(date_str: str) -> str:
    """Format an ASN1 date string to human-readable."""
    try:
        dt = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except ValueError:
        return date_str


def days_remaining(date_str: str) -> int:
    """Calculate days until certificate expiry."""
    try:
        dt = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")
        delta = dt - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        return delta.days
    except ValueError:
        return 0


def display_cert(host: str, port: int = 443) -> None:
    """Display certificate information."""
    try:
        cert = get_cert_info(host, port)
    except Exception as e:
        print(f"error: could not retrieve certificate for {host}:{port} — {e}", file=sys.stderr)
        sys.exit(1)

    subject = dict(x[0] for x in cert.get("subject", []))
    issuer = dict(x[0] for x in cert.get("issuer", []))
    not_before = cert.get("notBefore", "unknown")
    not_after = cert.get("notAfter", "unknown")
    sans = [x[1] for x in cert.get("subjectAltName", ())]

    print(f"Host:            {host}:{port}")
    print(f"Subject:         {subject.get('commonName', 'N/A')}")
    print(f"Issuer:          {issuer.get('commonName', 'N/A')}")
    print(f"Valid from:      {format_date(not_before)}")
    print(f"Valid until:     {format_date(not_after)}")
    print(f"Days remaining:  {days_remaining(not_after)}")
    print(f"Serial:          {cert.get('serialNumber', 'N/A')}")
    print(f"Algorithm:       {cert.get('signatureAlgorithm', 'N/A')}")
    print(f"SANs ({len(sans)}):")
    for san in sans:
        print(f"  - {san}")


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="SSL/TLS certificate checker — inspect expiry, issuer, and SANs.",
        epilog="Example: manta-cert example.com",
    )
    parser.add_argument("host", help="Hostname to check")
    parser.add_argument("-p", "--port", type=int, default=443, help="Port (default: 443)")
    args = parser.parse_args(argv)

    display_cert(args.host, args.port)


if __name__ == "__main__":
    main()
