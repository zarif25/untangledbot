class StoryExtractionError(Exception):
    def __init__(self, content_name, story_url, reason) -> None:
        super().__init__(
            f"Can't find {content_name} for {story_url} because: {reason}")


def does_not_exist_check(content_name):
    def wrapper1(func):
        def wrapper2(self, *args):
            try:
                return func(self, *args)
            except (AttributeError, TypeError) as e:
                raise StoryExtractionError(content_name, self.name, e)
        return wrapper2
    return wrapper1
