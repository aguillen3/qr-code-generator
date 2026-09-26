# QR code generator

Generate a black and white PNG QR code from a URL passed when you run the script. It uses high error correction and automatically sizes the code to fit the URL.

## Setup

Python 3.9 or later is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`, then run `python` in place of `python3` below.

## Usage

```bash
python3 generate_qr.py "https://thesquareriggerpub.com/pdf/Laocai Menu.pdf" -o LaocaiMenu.png
```

The URL is required. `-o` or `--output` is optional; the default file is `qr-code.png` in the current directory. Give URLs containing spaces, `&`, or `?` in quotes so the shell passes the whole URL. Spaces in the path are encoded as `%20` inside the QR code. The program accepts HTTP and HTTPS URLs and creates an output directory when needed:

```bash
python3 generate_qr.py "https://example.com/menu?source=table&campaign=summer" --output output/menu.png
```

For help, run `python3 generate_qr.py --help`. The script prints the exact URL embedded in the QR code. Test the image with a phone before printing, and confirm that the target page is publicly accessible. A QR code stores the supplied URL directly: changing its destination later requires generating a new image unless the URL points to a redirect you control.

## Files

- `generate_qr.py` — command-line generator.
- `requirements.txt` — Python package dependency.
- `.gitignore` — ignores local environments, caches, and default/generated output directories.

Custom PNG names outside `output/` can be committed intentionally; add them to `.gitignore` if they should remain local.
