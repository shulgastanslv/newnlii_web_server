from enum import Enum

class FeedFilter(str, Enum):
    foryou = "foryou"
    all = "all"
    following = "following"
    popular = "popular"
    new = "new"