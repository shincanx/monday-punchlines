"""Monday Morning Punchlines -- make.fun entry.

Writes a single joke about Monday mornings (at most 200 characters) to
entry.txt in the output directory. Deterministic, no network, no
randomness, no input.

The joke: "My weekend was just a free trial -- Monday is the paywall."
The weekend-as-free-trial setup reframes Monday morning as the moment the
subscription kicks in: the punchline lands on "paywall", a word nobody
expects in a Monday joke, and it stays economical (57 characters) while
being unmistakably about Monday morning itself.
"""

import os

# The entry: one joke about Monday mornings. 57 characters, under the 200 cap.
JOKE = "My weekend was just a free trial \u2014 Monday is the paywall."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(JOKE) > 200:
        raise ValueError(f"joke is {len(JOKE)} characters, over the 200 cap")
    if not JOKE.strip():
        raise ValueError("entry must not be only whitespace")
    if "monday" not in JOKE.lower():
        raise ValueError("entry must really be about Monday mornings")
    if "\n" in JOKE or "\r" in JOKE:
        # Craft: a single joke is a single line -- no hidden second setup.
        raise ValueError("entry must be a single line")
    if not JOKE.endswith("."):
        raise ValueError("entry must end with a full stop, the punchline's landing")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(JOKE + "\n")

    # Round-trip check: what landed on disk is exactly the joke.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != JOKE:
        raise ValueError("entry.txt does not match the joke")

    print(f"wrote {len(JOKE)} characters to {path}")


if __name__ == "__main__":
    main()
