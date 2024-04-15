from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        play_button = Button(text='Играть')
        settings_button = Button(text='Настройки')
        exit_button = Button(text='Выход')

        play_button.bind(on_press=self.start_game)
        settings_button.bind(on_press=self.open_settings)
        exit_button.bind(on_press=self.exit_game)

        self.add_widget(play_button)
        self.add_widget(settings_button)
        self.add_widget(exit_button)

    def start_game(self, instance):
        print("Начать игру")

    def open_settings(self, instance):
        print("Открыть настройки")

    def exit_game(self, instance):
        print("Выход из игры")
        App.get_running_app().stop()


class GameApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    GameApp().run()
