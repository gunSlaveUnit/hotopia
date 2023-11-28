from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


class ViewManager(ScreenManager):
    pass


class SignInView(Screen):
    pass


class SignUpView(Screen):
    pass


class Menu(Widget):
    pass


class Home(Screen):
    pass


class Explore(Screen):
    pass


class Profile(Screen):
    pass


class Hotopia(App):
    def __init__(self):
        super().__init__()

        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '800')

    def build(self):
        root_widget = Builder.load_file("main.kv")
        return root_widget


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
