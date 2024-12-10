from tools.social_media_browser.browser import create_browser
from tools.social_media_browser.user import User
from tools.social_media_browser.states import App
import tools.social_media_browser.settings as settings


def save_instagram_recent_chats() -> User:
    username = input("Username: ")
    password = input("Password: ")
    browser = create_browser(
        app=App.instagram,
        login_url=settings.INSTAGRAM_LOGIN_URL,
        home_url=settings.INSTAGRAM_HOME_URL,
        poi_url=settings.INSTAGRAM_INBOX_URL
    )
    user = User(username=username, password=password, browser=browser)
    user.login().open_point_of_interest().save_recent_chat_info()
    return user
