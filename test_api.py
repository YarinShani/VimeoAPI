
import pytest

from decouple import config
from main import post_new_comment, get_all_comments, delete_comment, search_comment_web_ui, quit_browser


user_name = config('user_name')

video_id = 257798097
comment_text = "Great Video!"


@pytest.fixture(autouse=True)
def setup():
    res = post_new_comment(video_id, comment_text)
    assert is_request_succeeded(res.status_code)
    comment_uri = res.json().get("uri")[1:]

    yield

    res = delete_comment(comment_uri)
    assert is_request_succeeded(res.status_code)


def test_post_new_comment_e2e():
    res = get_all_comments(video_id)
    assert is_request_succeeded(res.status_code)

    comments = json_comments_to_list(res.json().get("data"))
    assert search_comment(comments)


def json_comments_to_list(json_comments):
    return list(map(lambda a: a.get("text") + " by: " + a.get("user").get("name"), json_comments))


def test_search_comment_with_web_ui():
    try:
        articles = search_comment_web_ui(video_id)
        assert search_comment(map(lambda a: a.text, articles), comment_text)
    except Exception as e:
        print(e)
    finally:
        quit_browser()


def search_comment(comments):
    for comment in comments:
        if user_name in comment and comment_text in comment:
            return True

    return False


def is_request_succeeded(status_code):
    return 200 <= status_code <= 299

