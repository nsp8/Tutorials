from dataclasses import dataclass, field
from pathlib import Path
import json
from tools.social_media_browser.browser import Browser
from tools.social_media_browser.states import App, States
import tools.social_media_browser.settings as settings
from tools.social_media_browser.utils import get_latest_file_version, update_contents


@dataclass
class User:
    browser: Browser = field(default_factory=Browser)
    current_state: States = field(default=States.not_authenticated)

    def login(self, username, password):
        if not username:
            username = input("Enter your username: ")
        if not password:
            password = input("Enter your password: ")
        # self.browser.create_options(settings.HEADLESS, settings.DETACHED, settings.GPU_DISABLED)
        if self.browser.application.app_name == App.instagram:
            self.browser.authenticate_together(username, password)
            self.browser.reject_save_login()
            # TODO: find a way to find if user is authenticated
            self.current_state = States.authenticated
        elif self.browser.application.app_name == App.twitter:
            self.browser.authenticate(username, password)
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

    def save_recent_chat_info(self, store_new: bool = False):
        print("Saving recent chats ...")
        recent_chats = self.browser.get_inbox_latest()
        dir_path = Path(__file__).parent
        file_version = get_latest_file_version(dir_path)
        file_name = settings.INSTAGRAM_OUTPUT_FILENAME_PREFIX
        output_location = Path(f"{dir_path}/output")
        if not output_location.exists():
            output_location.mkdir()
        file_path = f"{output_location}/{file_name}_{file_version}.json"
        old_contents = dict()
        if Path(file_path).exists():
            print("\tFound chat history!")
            with open(file_path, "r") as r:
                old_contents.update(json.load(r))
        if store_new:
            file_path = f"{output_location}/{file_name}_{file_version + 1}.json"
            with open(file_path, "w") as n:
                print("Saving data in new file ...")
                json.dump(recent_chats, n, indent=2)
        else:
            print("Updating contents ...")
            updated = update_contents(old_contents, recent_chats)
            with open(file_path, "w") as w:
                print("\tWriting updated contents ...")
                json.dump(updated, w, indent=2)
