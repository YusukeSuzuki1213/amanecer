from typing import List

# twitter_id to dmm_id
dict = {
}

# TODO: Repository等用意


def get_dmm_id_by_twitter_id(twitter_id: int) -> int:
    return dict[twitter_id]


def get_follow_list() -> List[str]:
    return list(
        map(
            lambda key: str(key),
            dict.keys()
        )
    )
