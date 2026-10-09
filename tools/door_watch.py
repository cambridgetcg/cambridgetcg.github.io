#!/usr/bin/env python3
"""Check that every public door still answers.

Reads one URL per line from the given file (blank lines and lines starting
with '#' are ignored; anything after the URL on a line is a label). A door is
open if a GET, following redirects, ends in a 2xx response. A door that fails
is retried once after a pause, so one network blip does not raise an alarm.

Writes a Markdown report to stdout and exits 1 if any door stays dark.
"""
import sys
import time
import urllib.error
import urllib.request

TIMEOUT = 25
RETRY_PAUSE = 30
USER_AGENT = "door-watch/1.0 (+https://cambridgetcg.github.io/)"


def check(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, None
    except urllib.error.HTTPError as error:
        return error.code, None
    except Exception as error:  # DNS, TLS, timeout: the door did not answer
        return None, type(error).__name__


def is_open(status):
    return status is not None and 200 <= status < 300


def read_doors(path):
    doors = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            url, _, label = line.partition(" ")
            doors.append((url, label.strip()))
    return doors


def main():
    doors = read_doors(sys.argv[1])
    results = {url: check(url) for url, _ in doors}
    failing = [url for url, (status, _) in results.items() if not is_open(status)]
    if failing:
        time.sleep(RETRY_PAUSE)
        for url in failing:
            results[url] = check(url)

    dark = [(url, label) for url, label in doors if not is_open(results[url][0])]
    print(f"# Door watch\n\n{len(doors) - len(dark)} of {len(doors)} doors open.\n")
    if dark:
        print("## Dark\n")
        for url, label in dark:
            status, error = results[url]
            print(f"- {url} — {status or error}" + (f" ({label})" if label else ""))
        print()
    print("## Open\n")
    for url, label in doors:
        if is_open(results[url][0]):
            print(f"- {url}" + (f" ({label})" if label else ""))
    return 1 if dark else 0


if __name__ == "__main__":
    sys.exit(main())
