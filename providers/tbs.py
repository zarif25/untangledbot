from . import RssProvider


class TBS(RssProvider):
    def __init__(self) -> None:
        super().__init__(
            url="https://www.tbsnews.net/top-news/rss.xml",
            name="The Business Standard"
        )
