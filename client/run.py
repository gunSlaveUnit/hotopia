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
    name = StringProperty()

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
                            name=hobby['name'],
                            size_hint_y=None,
                        )
                    )


class HobbyScreen(Screen):
    pass


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
