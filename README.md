# The Doors

This repository serves https://cambridgetcg.github.io/: public copies of pages
that were public until 25 September 2026, when the repositories behind them
became private. Each door is back at its old address. The source repositories
stay private; this repository holds only what each door showed visitors.

## What a copy contains

Each door is copied from the last commit its old site was built from. Before a
copy goes in, it loses:

- hidden files and folders (agent hooks, CI configuration, local settings);
- repository instructions for agents, and personal pages and passages;
- local file paths, runtime details and personal email addresses;
- links into private source. Where a page invited you to clone or read the
  source, it now says the source is kept private.

[doors.json](doors.json) records, for every door, the private repository and
commit it came from and how many items were left out. What was left out is
not described here, because describing it would publish it.

A few old addresses now point to their newer homes, and some doors were not
restored. Pages that are mostly personal, and the citizen pages, wait for a
separate decision.

## How it is built

`jekyll/<door>/` holds doors that GitHub Pages built with Jekyll. The
[build workflow](.github/workflows/pages.yml) runs each of them through
GitHub's own Pages builder with `baseurl: /<door>`. `static/<door>/` holds doors
that were already plain files. Before deploying, the workflow refuses to
publish hidden files, personal email addresses, local paths and anything that
looks like a credential, and it runs gitleaks over the built site.

To update the doors, stage reviewed copies and run:

    python3 tools/assemble.py STAGE_DIR APPROVED_SLUGS_FILE DESCRIPTIONS_JSON

## Door watch

[door-watch](.github/workflows/door-watch.yml) checks every door in
[watch/doors.txt](watch/doors.txt) once a day. That covers the doors here and
the estate's other public sites. While any door is dark, one issue labelled
`door-dark` stays open with the current report. It closes itself when every
door answers again.

## Door check

After the knock, door-watch runs
[tools/door_contract.py](tools/door_contract.py) over the public doors in
[watch/contract.json](watch/contract.json). It checks, from outside, the
promises those doors make: history marked as history and asked out of
training, data responses that carry only data, the same bytes whatever name a
caller wears, plain refusals instead of traps, true 404s, links that resolve,
and public repositories whose clones run nothing on their own. Each item reads
PASS, FAIL or NOT CHECKED, and the run summary opens with one dated line that
says how long it stays valid. The step only reports: it never fails the job,
opens no issue and commits nothing.

It is the owner's monitor, not a crawler. It reads the household's own
history paths on purpose, as their keeper, although robots.txt asks unnamed
crawlers to stay out of them. It sends at most 12 requests to an origin a
day, waits 2 s between requests to one origin (honouring `Crawl-delay: 2`),
and names itself in its User-Agent. Its fixtures are in [tests/](tests/):

    python3 -m unittest discover -s tests

Each door keeps the license it was published under in its source repository.
