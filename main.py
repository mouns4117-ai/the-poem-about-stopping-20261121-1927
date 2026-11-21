"""Write the poem about stopping to /output/entry.txt.

Reads poem.txt from beside this file and copies its exact bytes to the
grader's output directory. Python 3.13, standard library only, no network,
fully deterministic: the same input always produces the same output bytes.
"""

import os
import sys


POEM_FILE = "poem.txt"
MIN_CHARS = 1
MAX_CHARS = 280


def read_poem():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, POEM_FILE), "rb") as handle:
        return handle.read()


def check_gate(data):
    text = data.decode("utf-8")
    points = len(text)
    if not (MIN_CHARS <= points <= MAX_CHARS):
        raise SystemExit(
            "poem is %d code points, outside the %d-%d gate"
            % (points, MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise SystemExit("poem must not be only white space")
    return data


def empty_dir_contents(path):
    # The grader's /output is a mounted directory: clear what is inside it,
    # never remove the directory itself.
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isdir(full) and not os.path.islink(full):
            for sub in os.listdir(full):
                os.remove(os.path.join(full, sub))
            os.rmdir(full)
        else:
            os.remove(full)


def main():
    data = check_gate(read_poem())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    empty_dir_contents(out_dir)
    with open(os.path.join(out_dir, "entry.txt"), "wb") as handle:
        handle.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
