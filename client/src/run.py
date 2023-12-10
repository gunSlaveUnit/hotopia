from typing import List

import requests
from kivy import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty

from client.src.settings import HOBBIES_URL, MEDIA_URL, MODULES_URL, UNITS_URL

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
        self.ids.hobbies.clear_widgets()

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
        self.map_modules(self.fetch_modules(hobby_id))

    def fetch_hobby(self, hobby_id: int) -> None:
        response = requests.get(f'{HOBBIES_URL}/{hobby_id}')
        if response.ok:
            hobby = response.json()
            self.title = hobby["name"]
            self.long_description = hobby["long_description"]

    @staticmethod
    def fetch_modules(hobby_id: int) -> List[dict]:
        response = requests.get(f'{MODULES_URL}/', params={"hobby_id": hobby_id})
        if response.ok:
            return response.json()

    def map_modules(self, extracted_modules: List[dict]) -> None:
        sorted_modules = sorted(
            extracted_modules,
            key=lambda item: (item['previous_module_id'] is not None, item['previous_module_id'])
        )

        self.ids.modules.clear_widgets()

        for module in sorted_modules:
            self.ids.modules.add_widget(
                ModuleCard(
                    item_id=module["id"],
                    title=module["name"],
                    description=module["description"],
                )
            )


class UnitCard(ButtonBehavior, MDBoxLayout):
    item_id = NumericProperty()
    title = StringProperty()


class ModuleScreen(MDScreen):
    title = StringProperty()
    next_unit_id = NumericProperty()
    selected_unit_id = NumericProperty()

    def load(self, module_id):
        self.fetch_module(module_id)
        self.units = self.fetch_units(module_id)
        self.map_units(self.units)

    def fetch_module(self, module_id: int) -> None:
        response = requests.get(f'{MODULES_URL}/{module_id}')
        if response.ok:
            module = response.json()
            self.title = module["name"]

    @staticmethod
    def fetch_units(module_id: int) -> List[dict]:
        response = requests.get(f'{UNITS_URL}/', params={"module_id": module_id})
        if response.ok:
            return response.json()

    def map_units(self, extracted_units: List[dict]) -> None:
        sorted_units = sorted(
            extracted_units,
            key=lambda item: (item['previous_unit_id'] is not None, item['previous_unit_id'])
        )

        self.ids.units.clear_widgets()

        for unit in sorted_units:
            self.ids.units.add_widget(
                UnitCard(
                    item_id=unit["id"],
                    title=unit["name"],
                )
            )

    def set_next_unit_by_selected(self):
        for unit in self.units:
            if unit['previous_unit_id'] == self.selected_unit_id:
                self.next_unit_id = unit['id']
                return
        self.next_unit_id = -1


class UnitScreen(MDScreen):
    title = StringProperty()
    filename = StringProperty()

    def load(self, unit_id):
        self.fetch_unit(unit_id)
        self.map_content(self.fetch_content(self.filename))

    def fetch_unit(self, unit_id: int) -> None:
        response = requests.get(f'{UNITS_URL}/{unit_id}')
        if response.ok:
            unit = response.json()
            self.title = unit["name"]
            self.filename = unit["content_filename"]

    @staticmethod
    def fetch_content(filename) -> str:
        response = requests.get(f'{MEDIA_URL}/{filename}')
        if response.ok:
            return response.text

    def map_content(self, content: str) -> None:
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(Builder.load_string(content))


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
