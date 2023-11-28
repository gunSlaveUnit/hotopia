from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class SignInView(Screen):
    pass


class SignUpView(Screen):
    pass


ROOT_WIDGET = Builder.load_file("main.kv")


class Hotopia(App):
    def build(self):
        return ROOT_WIDGET


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
