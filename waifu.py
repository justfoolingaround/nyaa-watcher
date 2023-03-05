import time
from datetime import datetime, timedelta, timezone

import anitopy
import click
import httpx
import humanize
import regex
from animdl.utils import http_client

from core import DiscordNoises, TerminalNoises

session = httpx.Client()

http_client.integrate_ddg_bypassing(session, ".nyaa.si")

NYAA_URL = "https://nyaa.si/"

NYAA_RE = regex.compile(
    r"<item>\s+"
    r"<title>(?P<title>.+?)</title>.+?"
    r"<guid .+?>(?P<url>.+?)</guid>.+?"
    r"<pubDate>(?P<date_published>.+?)</pubDate>.+?"
    r"<nyaa:seeders>(?P<seeds>.+?)</nyaa:seeders>.+?"
    r"<nyaa:leechers>(?P<leeches>.+?)</nyaa:leechers>.+?"
    r"<nyaa:downloads>(?P<downloads>.+?)</nyaa:downloads>.+?"
    r"<nyaa:infoHash>(?P<infohash>.+?)</nyaa:infoHash>.+?"
    r"</item>",
    flags=regex.DOTALL,
)


@click.command()
@click.argument("query")
@click.option(
    "--discord",
    "-d",
    help="Output to a Discord webhook instead of stdout.",
    required=False,
)
@click.option(
    "--run-for",
    "-r",
    help="Run the command for a specific amount of time.",
    default=3600,
)
@click.option(
    "--interval",
    "-i",
    help="Interval between each run.",
    default=180,
)
def waifu(query, discord, run_for, interval):

    run_until = datetime.now() + timedelta(seconds=run_for)

    if discord:
        noises = DiscordNoises(query, run_until, interval, session, discord)
    else:
        noises = TerminalNoises(query, run_until, interval)

    noises.introduce()

    pattern = regex.compile(
        r"(.*?)".join(map(regex.escape, query.strip())),
        flags=regex.IGNORECASE,
    )

    info_hashes = set()

    while datetime.now() < run_until:
        response = session.get(
            NYAA_URL,
            params={"f": 0, "c": "1_0", "q": query, "page": "rss"},
        )

        torrent_list = []
        first_blood = not bool(info_hashes)

        for match in NYAA_RE.finditer(response.text):
            if match["infohash"] in info_hashes:
                continue

            info_hashes.add(match["infohash"])

            date = datetime.strptime(
                match["date_published"], "%a, %d %b %Y %H:%M:%S %z"
            )

            if date < datetime.now(timezone.utc) - timedelta(days=1):
                continue

            title = anitopy.parse(match["title"]).get("anime_title")

            if title is not None and pattern.search(title):
                torrent_list.append(
                    f"**{match['title']}**, uploaded {humanize.naturaldate(date)} @ {date:%Y-%m-%d %H:%M:%S}\n"
                    f"**Seeds, Leeches, Completed:** {match['seeds']}, {match['leeches']}, {match['downloads']}\n"
                    f"🔗 {match['url']} 🧲 `magnet:?xt=urn:btih:{match['infohash']}`",
                )

        if first_blood and torrent_list:
            noises.say(
                f"While I did find {len(torrent_list)} results, usually first results could get spammy! I'm notifying just as a warning that the anime may already be out!"
            )

        else:

            if torrent_list:
                noises.say(
                    f"Hey hey, found {len(torrent_list)} results~!\n\n"
                    + "\n".join(torrent_list)
                )

        time.sleep(interval)

    noises.say("Oyasumi weebs, see you back again next time!")


if __name__ == "__main__":
    waifu()
