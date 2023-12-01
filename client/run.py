from kivy import Config
from kivy.app import App
from kivy.lang import Builder
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


class ExploreScreen(Screen):
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
