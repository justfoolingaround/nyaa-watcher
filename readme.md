<h1 align="center">Anime Waifu<sub><sub>aka, Nyaa watcher</sub></sub></h1>

Scan [Nyaa](https://nyaa.si/) periodically for a fresh anime episode.

It is highly recommended to use this project with a cron job around the weekly time when an anime is out!

## Usage

```console
$ py waifu.py --help
Usage: waifu.py [OPTIONS] QUERY

Options:
  -d, --discord TEXT      Output to a Discord webhook instead of stdout.
  -r, --run-for INTEGER   Run the command for a specific amount of time.
  -i, --interval INTEGER  Interval between each run.
  --help                  Show this message and exit.
```

And, with an anime:

```console
$ py waifu.py "attack on weebs"
Moshi moshi weebs, I'm Kei and I'll now be watching over 'attack on weebs' uploads on Nyaa for 59 minutes from now every 180 seconds.

While I did find 1 results, usually first results could get spammy! I'm notifying just as a warning that the anime may already be out!
```