import os
import requests

HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_CREATED = 201
HTTP_STATUS_CODE_PARTIAL_CONTENT = 206

HEROKU_BASE_URL = "https://api.heroku.com/apps"


def get_latest_slug(app_name, api_key):
    """
    Returns the currently deployed slug
    :param app_name: Heroku app name
    :param api_key: Heroku api key
    :return:
    """
    result = requests.get(f"{HEROKU_BASE_URL}/{app_name}/releases",
                          headers={
                              "Accept": "application/vnd.heroku+json; version=3",
                              "Authorization": f"Bearer {api_key}",
                              "Content-Type": "application/json",
                              "Range": "version ..; max=1, order=desc"
                          })
    if result.status_code != HTTP_STATUS_CODE_PARTIAL_CONTENT:
        raise Exception(f"Could not fetch latest release from Heroku: {result.content}")

    return result.json()[0]["slug"]["id"]


def get_slug_tarball_url(app_name, slug_id, api_key):
    """
    Returns the url of the tarball of a given slug
    :param app_name: Heroku app name
    :param slug_id: Heroku slug id
    :param api_key: Heroku api key
    :return:
    """
    result = requests.get(f"{HEROKU_BASE_URL}/{app_name}/slugs/{slug_id}",
                          headers={
                              "Accept": "application/vnd.heroku+json; version=3",
                              "Authorization": f"Bearer {api_key}",
                              "Content-Type": "application/json",
                          })
    if result.status_code != HTTP_STATUS_CODE_OK:
        raise Exception(f"Could not fetch slug tarball from Heroku: {result.content}")

    return result.json()["blob"]["url"]


def create_new_build(app_name, tarball_url, api_key):
    """
    Creates a new Heroku build.
    :param app_name: Heroku app name
    :param tarball_url: Tarball Url
    :param api_key: Heroku api key
    :return:
    """
    result = requests.post(f"{HEROKU_BASE_URL}/{app_name}/builds",
                          headers={
                              "Accept": "application/vnd.heroku+json; version=3",
                              "Authorization": f"Bearer {api_key}",
                              "Content-Type": "application/json",
                          }, json={
            "source_blob": {
                "url": tarball_url
            }
        })
    if result.status_code != HTTP_STATUS_CODE_CREATED:
        raise Exception(f"Could not create new Heroku build: {result.content}")


if __name__ == "__main__":
    APP_NAME = os.environ.get("INPUT_HEROKU_APP_NAME", None)
    API_KEY = os.environ.get("INPUT_HEROKU_API_KEY", None)

    all_settings_set = APP_NAME is not None and API_KEY is not None
    if all_settings_set:
        slug_id = get_latest_slug(APP_NAME, API_KEY)
        tarball_url = get_slug_tarball_url(APP_NAME, slug_id, API_KEY)
        create_new_build(APP_NAME, tarball_url, API_KEY)
        print(f"Rebuilding app {APP_NAME}")
    else:
        print("Error: APP_NAME or HEROKU_API_KEY not set.")
