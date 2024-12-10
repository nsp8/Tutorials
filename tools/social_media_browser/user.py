from dataclasses import dataclass, field
from pathlib import Path
import json
from tools.social_media_browser.browser import Browser
from tools.social_media_browser.states import App, States
import tools.social_media_browser.settings as settings
from tools.social_media_browser.utils import update_contents


@dataclass
class User:
    username: str
    password: str
    browser: Browser = field(default_factory=Browser)
    current_state: States = field(default=States.not_authenticated)

    def login(self):
        if not self.username:
            self.username = input("Enter your username: ")
        if not self.password:
            self.password = input("Enter your password: ")
        self.browser.create_options(settings.HEADLESS, settings.DETACHED, settings.GPU_DISABLED)
        if self.browser.application.app_name == App.instagram:
            self.browser.authenticate_together(self.username, self.password)
            self.browser.reject_save_login()
            # TODO: find a way to find if user is authenticated
            self.current_state = States.authenticated
        elif self.browser.application.app_name == App.twitter:
            self.browser.authenticate(self.username, self.password)
            # if self.browser.get_current_url() == settings.HOME_URL:
            if "home" in self.browser.get_current_url():
                self.current_state = States.authenticated

        return self

    def open_point_of_interest(self):
        if self.current_state is States.authenticated:
            self.browser.navigate_to(self.browser.application.poi_url)
            if self.browser.application.app_name == App.instagram:
                self.browser.reject_notifications()

        return self

    def save_recent_chat_info(self):
        recent_chats = self.browser.get_inbox_latest()
        file_path = f"{Path(__file__).parent}/user_data.json"
        old_contents = dict()
        if Path(file_path).exists():
            with open(file_path, "r") as r:
                old_contents.update(json.load(r))

        updated = update_contents(old_contents, recent_chats)
        with open(file_path, "w") as w:
            json.dump(updated, w, indent=2)
