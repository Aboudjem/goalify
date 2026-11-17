"""slugify: turn a title into a URL slug. The demo project that `make demo` verifies."""
import re


def slugify(title):
    """'Hello, World!' -> 'hello-world'. Lowercase, hyphens between words, nothing else."""
    words = re.findall(r"[a-z0-9]+", title.lower())
    return "-".join(words)
