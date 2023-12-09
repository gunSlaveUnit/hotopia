from typing import List

import requests
from kivy import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty

from client.src.settings import HOBBIES_URL, MEDIA_URL, MODULES_URL

# Don't move it from here.
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '800')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

from client.src.auth_service import AuthService
from api.v1.schemas.users import UserSignUpSchema, UserSignInSchema


class RootLayout(MDBoxLayout):
    pass


class SignInScreen(MDScreen):
    def sign_in(self):
        account_name = self.ids.account_name_input.text
        password = self.ids.password_input.text

        data = UserSignInSchema(
            account_name=account_name,
            password=password,
        )

        if hotopia.auth_service.sign_in(data).ok:
            hotopia.auth_service.me()
            hotopia.root.ids.explore_screen.load()
            hotopia.root.ids.screen_manager.current = "explore_screen"
            hotopia.root.ids.screen_manager.transition.direction = "up"


class SignUpScreen(MDScreen):
    def sign_up(self):
        email = self.ids.email_input.text
        account_name = self.ids.account_name_input.text
        password = self.ids.password_input.text

        data = UserSignUpSchema(
            email=email,
            account_name=account_name,
            password=password,
        )

        if hotopia.auth_service.sign_up(data).ok:
            hotopia.auth_service.me()
            hotopia.root.ids.explore_screen.load()
            hotopia.root.ids.screen_manager.current = "explore_screen"
            hotopia.root.ids.screen_manager.transition.direction = "up"


class HobbyCard(ButtonBehavior, MDBoxLayout):
    item_id = NumericProperty()
    title = StringProperty()
    short_description = StringProperty()
    picture_url = StringProperty()


class ExploreScreen(MDScreen):
    def load(self) -> None:
        self.ids.hobbies.clear_widgets()

        extracted_hobbies = self.fetch_hobbies()
        self.map_hobbies(extracted_hobbies)

    @staticmethod
    def fetch_hobbies() -> List[dict]:
        response = requests.get(HOBBIES_URL)
        if response.ok:
            return response.json()

    def map_hobbies(self, extracted_hobbies: List[dict]) -> None:
        for hobby in extracted_hobbies:
            self.ids.hobbies.add_widget(
                HobbyCard(
                    item_id=hobby["id"],
                    title=hobby["name"],
                    short_description=hobby["short_description"],
                    picture_url=f'{MEDIA_URL}/{hobby["card_picture_filename"]}',
                )
            )


class ModuleCard(ButtonBehavior, MDBoxLayout):
    item_id = NumericProperty()
    title = StringProperty()
    description = StringProperty()


class HobbyScreen(MDScreen):
    title = StringProperty()
    long_description = StringProperty()

    def load(self, hobby_id):
        self.fetch_hobby(hobby_id)
        self.fetch_modules(hobby_id)

    def fetch_hobby(self, hobby_id: int) -> None:
        response = requests.get(f'{HOBBIES_URL}/{hobby_id}')
        if response.ok:
            hobby = response.json()
            self.title = hobby["name"]
            self.long_description = hobby["long_description"]


class Hotopia(MDApp):
    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        self.default_margin = 16

    def build(self):
        root_layout = Builder.load_file("layout.kv")
        return root_layout


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
