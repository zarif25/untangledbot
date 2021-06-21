from . import RssProvider


class DStar(RssProvider):
    def __init__(self) -> None:
        super().__init__(
            url="https://www.thedailystar.net/top-news/rss.xml",
            name="The Daily Star"
        )
