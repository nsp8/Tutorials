from dataclasses import dataclass, field
from re import search
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import tools.social_media_browser.settings as settings
from tools.social_media_browser.states import App
import tools.social_media_browser.utils as utils


@dataclass
class Application:
    app_name: App
    login_url: str
    home_url: str
    poi_url: str


@dataclass
class BrowserOptions:
    is_detached: bool = settings.DETACHED
    is_headless: bool = settings.HEADLESS
    is_gpu_disabled: bool = settings.GPU_DISABLED


@dataclass
class Browser:
    wait_timeout: int = 30
    application: Application = field(default_factory=Application)
    driver: webdriver.Chrome = field(default_factory=webdriver.Chrome)
    options: Options = field(default_factory=Options)
    action_count: int = 0
    is_headless: bool = False

    def create_options(self, options: BrowserOptions):
        self.options = Options()
        if options.is_detached:
            self.options.add_experimental_option("detach", options.is_detached)
        if options.is_headless:
            self.is_headless = options.is_headless
            self.options.add_argument("--headless")
        if options.is_gpu_disabled:
            self.options.add_argument("--disable-gpu")
        return self

    def authenticate(self, username, password):
        self.driver = webdriver.Chrome(options=self.options)
        try:
            self.driver.get(self.application.login_url)
            print("---- Waiting for username ----")
            self.send_username(username)
            print("---- Waiting for password ----")
            self.send_password(password)
            # sleep(60)
        except NoSuchElementException as e:
            print(f">>> Encountered: {e}")
        except KeyboardInterrupt:
            print("// Terminating //")
            self.driver.quit()

    def authenticate_together(self, username, password):
        self.driver = webdriver.Chrome(options=self.options)
        try:
            self.driver.get(self.application.login_url)
            print("---- Waiting for username and password ----")
            self.send_credentials(username=username, password=password)
            # sleep(60)
        except NoSuchElementException as e:
            print(f">>> Encountered: {e}")
        except KeyboardInterrupt:
            print("// Terminating //")
            self.driver.quit()

    def locate_input_field(self):
        element = WebDriverWait(self.driver, self.wait_timeout).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "input"))
        )
        return element

    def locate_input_fields(self):
        elements = WebDriverWait(self.driver, self.wait_timeout).until(
            expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "input"))
        )
        return elements

    @utils.delay
    def send_username(self, username):
        username_input = self.locate_input_field()
        if username_input:
            print("\t---- Username is ready ----")
            username_input.send_keys(username + Keys.ENTER)

    @utils.delay
    def send_password(self, password):
        password_field = self.locate_input_fields()
        if len(password_field) == 2:
            print("\t---- Password is ready ----")
            # print(password_field)
            password_field[1].send_keys(password + Keys.ENTER)

    @utils.delay
    def send_credentials(self, username, password):
        username_input, password_input = self.locate_input_fields()
        if username_input and password_input:
            print("\t---- Username and password fields are ready ----")
            username_input.send_keys(username)
            password_input.send_keys(password + Keys.ENTER)

    @utils.delay
    def get_current_url(self):
        print(self.driver.current_url)
        return self.driver.current_url

    @utils.delay
    def navigate_to(self, url: str):
        self.driver.get(url)

    @utils.delay
    def reject_save_login(self):
        # TODO: find a way to call this in a separate thread
        buttons = WebDriverWait(self.driver, self.wait_timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[role='button']")
            )
        )
        if buttons:
            for e, w in zip(buttons, map(lambda el: el.text, buttons)):
                if w.strip().lower() == "not now":
                    print("Not saving login info ...")
                    e.click()

    @utils.delay
    def reject_notifications(self):
        # TODO: find a way to call this in a separate thread
        buttons = WebDriverWait(self.driver, self.wait_timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (By.TAG_NAME, "button")
            )
        )
        if buttons:
            for e, w in zip(buttons, map(lambda el: el.text, buttons)):
                if w.strip().lower() == "not now":
                    print("Rejecting notifications ...")
                    e.click()

    @utils.delay
    def get_inbox_latest(self):
        # TODO: Get more chats
        chat_contents = dict()
        buttons = WebDriverWait(self.driver, self.wait_timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[role='button']")
            )
        )
        chat_elements = [
            el for el in buttons if search("user avatar", el.accessible_name.lower())
        ]
        for chat in chat_elements:
            chat.click()
            data = self.driver.find_element(
                By.XPATH,
                "//div[contains(@aria-label, 'Conversation with ')]"
            )
            text_split = data.text.split("\n")
            name = text_split[0]
            contents = [t for t in text_split[1:] if t.strip()]
            chat_id = self.get_current_url().split("/")[-2]
            chat_contents[chat_id] = {"name": name, "contents": contents}
        while not chat_contents and self.action_count < 10:
            self.action_count += 1
            self.get_inbox_latest()
        self.action_count = 0
        return chat_contents

    def close(self):
        self.driver.quit()


def create_browser(app: App, login_url, home_url, poi_url, options: BrowserOptions):
    app = Application(
        app_name=app, login_url=login_url, home_url=home_url, poi_url=poi_url
    )
    return Browser(application=app).create_options(options=options)
