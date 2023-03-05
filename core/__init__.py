import random

import humanize
from rich.console import Console


class WaifuNoises:

    classified_name = "Kei"

    def __init__(self, query, run_until, interval) -> None:
        self.query = query
        self.run_until = run_until
        self.interval = interval

    @property
    def introduction_text(self):
        return (
            f"Moshi moshi weebs, I'm {self.classified_name} and I'll now be watching over "
            f"{self.query!r} uploads on Nyaa for {humanize.naturaltime(self.run_until)} every {self.interval} seconds.\n"
        )

    def say(self, text):
        raise NotImplementedError

    def introduce(self):
        raise NotImplementedError


class TerminalNoises(WaifuNoises):
    def __init__(self, query, run_until, interval) -> None:
        super().__init__(query, run_until, interval)

        self.console = Console(stderr=True)

    def say(self, text):
        self.console.print(text)

    def introduce(self):
        self.console.print(self.introduction_text, style="bold green")


class DiscordNoises(WaifuNoises):

    light_hex_colors = (
        0xF8B195,
        0xF67280,
        0xC06C84,
        0x6C5B7B,
        0x355C7D,
        0x99B898,
        0xFECEAB,
        0xFF847C,
        0xE84A5F,
    )

    def __init__(self, query, run_until, interval, session, webhook) -> None:
        super().__init__(query, run_until, interval)

        self.session = session
        self.webhook = webhook

    def say(self, text):

        self.session.post(
            self.webhook,
            json={
                "embeds": [
                    {
                        "color": random.choice(self.light_hex_colors),
                        "description": text,
                    }
                ],
            },
        )

    def introduce(self):
        self.say(self.introduction_text)
