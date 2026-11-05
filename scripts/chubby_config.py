"""Local-only validation for Office's scoped Anthropic Messages gateway."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

DEFAULT_BASE_URL = ""  # Deployment endpoint must be configured explicitly.


def validate_config(api_key: str, base_url: str, model: str) -> str:
    # Never include supplied values in errors: malformed config can be a secret.
    if not re.fullmatch(r"cbm_[a-f0-9]{64}", api_key):
        raise ValueError("CHUBBY_API_KEY must be a scoped cbm_ Claude Code key")
    try:
        url = urlsplit(base_url)
        valid = (url.scheme == "https" and bool(url.hostname) and not url.username
                 and not url.password and not url.query and not url.fragment
                 and url.path.rstrip("/") == "/office/api/chubby"
                 and not any(c.isspace() or ord(c) < 32 for c in base_url)
                 and "\\" not in base_url and url.port in (None, 443))
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("CHUBBY_BASE_URL must be an HTTPS Office /office/api/chubby URL without /v1, credentials, query, or fragment")
    if not re.fullmatch(r"[a-z][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._/-]*", model):
        raise ValueError("Chubby requires a qualified exact model ID, not a Claude alias")
    return base_url.rstrip("/")
