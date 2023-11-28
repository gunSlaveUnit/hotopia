from kivy.app import App
from kivy.lang import Builder

ROOT_WIDGET = Builder.load_file("main.kv")


class Hotopia(App):
    def build(self):
        return ROOT_WIDGET


if __name__ == '__main__':
    hotopia = Hotopia()
    hotopia.run()
