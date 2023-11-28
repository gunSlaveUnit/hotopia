from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class ViewManager(ScreenManager):
    pass


class SignInView(Screen):
    pass


class SignUpView(Screen):
    pass


class Hotopia(App):
    def build(self):
        root_widget = Builder.load_file("main.kv")
        return root_widget


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
