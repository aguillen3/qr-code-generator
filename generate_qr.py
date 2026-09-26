#!/usr/bin/env python3
"""Generate a PNG QR code from a URL supplied on the command line."""

import argparse
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

import qrcode


def normalize_url(value: str) -> str:
    """Check an HTTP(S) URL and encode spaces and other unsafe path characters."""
    value = value.strip()
    try:
        parts = urlsplit(value)
        port = parts.port  # Also rejects malformed port numbers.
        del port
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid URL: {exc}") from exc
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise argparse.ArgumentTypeError("URL must start with http:// or https:// and include a hostname")
    if any(char.isspace() for char in parts.netloc):
        raise argparse.ArgumentTypeError("URL hostname cannot contain spaces")
    return urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/%:@!$&'()*+,;=-._~"),
                       quote(parts.query, safe="/%?:@!$&'()*+,;=-._~"),
                       quote(parts.fragment, safe="/%?:@!$&'()*+,;=-._~")))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QR code PNG for a URL.")
    parser.add_argument("url", type=normalize_url, help="Destination URL (put it in quotes if it contains spaces or &)")
    parser.add_argument("-o", "--output", type=Path, default=Path("qr-code.png"), help="Output PNG path (default: qr-code.png)")
    args = parser.parse_args()
    if args.output.suffix.lower() != ".png":
        parser.error("output filename must end in .png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(args.url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"Saved {args.output} for {args.url}")


if __name__ == "__main__":
    main()
