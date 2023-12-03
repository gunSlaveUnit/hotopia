import asyncio

import aiohttp
from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu = Menu()

    def add_menu(self):
        self.add_widget(self.menu)

    def remove_menu(self):
        self.remove_widget(self.menu)


class SignInScreen(Screen):
    pass


class SignUpScreen(Screen):
    pass


class HobbyCard(ButtonBehavior, BoxLayout):
    item_id = NumericProperty()
    title = StringProperty()
    short_description = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExploreScreen(Screen):
    def on_enter(self, *args):
        self.ids.hobbies.clear_widgets()
        asyncio.run(self.fetch_hobbies())

    async def fetch_hobbies(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/api/v1/hobbies') as response:
                hobbies = await response.json()

                for hobby in hobbies:
                    self.ids.hobbies.add_widget(
                        HobbyCard(
                            item_id=hobby['id'],
                            title=hobby['name'],
                            short_description=hobby['short_description'],
                        )
                    )


class ModuleCard(ButtonBehavior, BoxLayout):
    item_id = NumericProperty()
    title = StringProperty()
    description = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HobbyScreen(Screen):
    title = StringProperty()
    long_description = StringProperty()

    def load(self, hobby_id):
        self.ids.modules.clear_widgets()
        asyncio.run(self.fetch_hobby(hobby_id))

    async def fetch_hobby(self, hobby_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://127.0.0.1:8000/api/v1/hobbies/{hobby_id}') as response:
                hobby = await response.json()
                self.title = hobby['name']
                self.long_description = hobby['long_description']

            async with session.get(f'http://127.0.0.1:8000/api/v1/modules/?hobby_id={hobby_id}') as response:
                modules = await response.json()

                for module in modules:
                    self.ids.modules.add_widget(
                        ModuleCard(
                            item_id=module['id'],
                            title=module['name'],
                            description=module['description'],
                        )
                    )


class UnitCard(ButtonBehavior, BoxLayout):
    item_id = NumericProperty()
    title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ModuleScreen(Screen):
    title = StringProperty()

    def load(self, module_id):
        self.ids.units.clear_widgets()
        asyncio.run(self.fetch_module(module_id))

    async def fetch_module(self, module_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://127.0.0.1:8000/api/v1/modules/{module_id}') as response:
                module = await response.json()
                self.title = module['name']

            async with session.get(f'http://127.0.0.1:8000/api/v1/units/?module_id={module_id}') as response:
                units = await response.json()

                for unit in units:
                    self.ids.units.add_widget(
                        UnitCard(
                            item_id=unit['id'],
                            title=unit['name'],
                        )
                    )


class UnitScreen(Screen):
    title = StringProperty()

    def load(self, unit_id):
        self.ids.content.clear_widgets()
        asyncio.run(self.fetch_unit(unit_id))

    async def fetch_unit(self, unit_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://127.0.0.1:8000/api/v1/units/{unit_id}') as response:
                unit = await response.json()
                self.title = unit['name']


class ProfileScreen(Screen):
    pass


class Menu(GridLayout):
    pass


class Hotopia(App):
    def __init__(self):
        super().__init__()

        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '800')

    def build(self):
        root_layout = Builder.load_file("layout.kv")
        return root_layout


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
