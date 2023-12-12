from typing import List, Optional

import requests
from kivy import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty

from api.v1.schemas.walkthroughes import WalkthroughCreateSchema
from client.src.settings import HOBBIES_URL, MEDIA_URL, MODULES_URL, UNITS_URL, WALKTHROUGHES_URL

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

    def fetch_hobbies(self) -> List[dict]:
        search_name = self.ids.search_input.text

        response = requests.get(
            HOBBIES_URL,
            params={"search": search_name if search_name != "" else None},
        )

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
        response = requests.get(f'{MODULES_URL}', params={"hobby_id": hobby_id})
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
    title = StringProperty()
    item_id = NumericProperty()
    is_done = BooleanProperty()


class ModuleScreen(MDScreen):
    units = ListProperty()
    title = StringProperty()

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
        response = requests.get(f'{UNITS_URL}', params={"module_id": module_id})
        if response.ok:
            return response.json()

    def map_units(self, extracted_units: List[dict]) -> None:
        sorted_units = sorted(
            extracted_units,
            key=lambda item: (item['previous_unit_id'] is not None, item['previous_unit_id'])
        )

        self.ids.units.clear_widgets()

        for unit in sorted_units:
            response = requests.get(
                f'{WALKTHROUGHES_URL}',
                params={
                    "user_id": hotopia.auth_service.current_user.id,
                    "unit_id": unit["id"]
                }
            )

            is_done = True if response.json() else False

            self.ids.units.add_widget(
                UnitCard(
                    is_done=is_done,
                    item_id=unit["id"],
                    title=unit["name"],
                )
            )


class UnitScreen(MDScreen):
    title = StringProperty()
    item_id = NumericProperty()
    filename = StringProperty()
    module_id = NumericProperty()
    is_unit_complete = BooleanProperty()
    complete_button_text = StringProperty()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.related_walkthrough_id: Optional[int] = None

    def load(self, unit_id):
        self.fetch_unit(unit_id)
        self.set_complete_button_text(unit_id)
        self.map_content(self.fetch_content(self.filename))

    def fetch_unit(self, unit_id: int) -> None:
        response = requests.get(f'{UNITS_URL}/{unit_id}')
        if response.ok:
            unit = response.json()
            self.item_id = unit["id"]
            self.title = unit["name"]
            self.filename = unit["content_filename"]
            self.module_id = unit["module_id"]

    def set_complete_button_text(self, unit_id: int) -> None:
        self.related_walkthrough_id = self.get_related_walkthrough_id(unit_id)

        if self.related_walkthrough_id:
            self.is_unit_complete = True
            self.complete_button_text = "Mark as undone"
        else:
            self.is_unit_complete = False
            self.complete_button_text = "Mark as done"

    @staticmethod
    def get_related_walkthrough_id(unit_id: int) -> Optional[int]:
        response = requests.get(
            f'{WALKTHROUGHES_URL}',
            params={
                "user_id": hotopia.auth_service.current_user.id,
                "unit_id": unit_id,
            }
        )

        if response.ok:
            if response.json():
                return response.json()[0]["id"]

        return None

    @staticmethod
    def fetch_content(filename) -> str:
        response = requests.get(f'{MEDIA_URL}/{filename}')
        if response.ok:
            return response.text

    def map_content(self, content: str) -> None:
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(Builder.load_string(content))

    def process_walkthrough(self):
        user_id = hotopia.auth_service.current_user.id

        data = WalkthroughCreateSchema(
            user_id=user_id,
            unit_id=self.item_id,
        )

        if self.is_unit_complete:
            requests.delete(f'{WALKTHROUGHES_URL}/{self.related_walkthrough_id}')
        else:
            requests.post(WALKTHROUGHES_URL, json=data.model_dump())

        self.set_complete_button_text(self.item_id)


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
