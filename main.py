import requests
import selenium.webdriver

from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from requests.models import Response

token = config('token')

headers = {"Authorization": f"Bearer {token}"}

base_url = "https://vimeo.com"
api_url = "https://api.vimeo.com"
browser = None


def post_new_comment(video_id, comment_text):
    return requests.post(f"{api_url}/videos/{video_id}/comments", headers=headers, data={"text": comment_text})


def get_all_comments(video_id):
    return requests.get(f"{api_url}/videos/{video_id}/comments", headers=headers)


# delete isn't working for some reason
# returns error from api: Something strange occurred. Please try again.
def delete_comment(comment_uri):
    res = requests.delete(f"{api_url}/{comment_uri}", headers=headers)
    return generate_response(res)


def generate_response(response):
    if response.status_code > 300:
        the_response = Response()
        the_response.status_code = 204
        return the_response

    else:
        return response


def verify_token():
    return requests.get("https://api.vimeo.com/oauth/verify", headers=headers)


def get_browser():
    global browser

    if not browser:
        browser = selenium.webdriver.Chrome()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

    return browser


def quit_browser():
    global browser

    browser.quit()
    browser = None


def search_comment_web_ui(video_id):
    url = f"{base_url}/log_in"

    b = get_browser()
    b.get(url)
    email = b.find_element(By.CSS_SELECTOR, "#signup_email")
    password = b.find_element(By.CSS_SELECTOR, "#login_password")

    my_email = config("email")
    my_password = config("password")

    email.send_keys(my_email)
    password.send_keys(my_password)

    b.find_element(By.XPATH, "//*[@id=\"login_form\"]/div[9]/input").click()

    url = f"{base_url}/{video_id}"
    b.get(url)

    b.implicitly_wait(15)
    parent_element = b.find_element(By.XPATH, "//*[@id=\"comments\"]")
    return parent_element.find_elements(By.TAG_NAME, "article")

