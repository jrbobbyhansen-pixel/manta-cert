# manta-cert

SSL/TLS certificate checker — inspect expiry, issuer, and Subject Alternative Names (SANs) from the command line.

Part of the [Manta](https://github.com/jrbobbyhansen-pixel) collection of zero-dependency Python CLI tools.

## Installation

```bash
pip install manta-cert
```

Or run directly:

```bash
python -m manta_cert --help
```

## Usage

```bash
# Check a certificate on default HTTPS port
manta-cert example.com

# Check a certificate on a custom port
manta-cert example.com -p 8443
```

### Example Output

```
Host:            example.com:443
Subject:         example.com
Issuer:          R3
Valid from:      2025-01-15 10:30:00 GMT
Valid until:     2026-02-15 10:30:00 GMT
Days remaining:  198
Serial:          04:AB:...
Algorithm:       sha256WithRSAEncryption
SANs (2):
  - example.com
  - www.example.com
```

## API

```python
from manta_cert import get_cert_info, format_date, days_remaining

info = get_cert_info("example.com")
print(info["subject"])
print(days_remaining(info["notAfter"]))
```

## License

MIT — see [LICENSE](LICENSE).
