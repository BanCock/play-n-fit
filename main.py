from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from random import random

# фафаыфафыафыафы
# Класс интерактивной картинки
class InteractiveImage(Widget):
    def __init__(self, image_path, rows, cols, **kwargs):
        super(InteractiveImage, self).__init__(**kwargs)
        # Количество строк и столбцов, путь к картинке
        self.rows = rows
        self.cols = cols
        self.image_path = image_path
        # Массив прямоугольников
        self.rectangles = []
        # Инициализация изображения и отрисовка прямоугольников
        self.init_image()
        self.draw_rectangles()


    def init_image(self):

    # Здесь рисуем холст, его фоном становится наша картинка, изменения размеров окна не приветствуется
    # так как в качестве размера берём размер окна, а не самой картинки
        with self.canvas:
            self.bg = Rectangle(source=self.image_path, pos=self.pos, size=Window.size)
            self.size = Window.size

# Функция отрисовки прямоугольников
    def draw_rectangles(self):
        with self.canvas:
            for row in range(self.rows):
                for col in range(self.cols):
                    Color(1, 1, 1, 0.8)  # Прозрачный цвет для секций
                    rect = Rectangle(pos=((self.width / self.cols) * col, (self.height / self.rows) * row),
                                     size=(self.width / self.cols, self.height / self.rows))
                    self.rectangles.append(rect)
            print(self.width, self.height)

# Функция, привязанная к нажатию на экран
    def on_touch_down(self, touch):
        super(InteractiveImage, self).on_touch_down(touch)
        # Проверка что нажатие внутри изображения
        if self.collide_point(*touch.pos):
            # Ширина столбца и высота строки считается как ширина и высота окна делить на их количество
            col_width = self.width / self.cols
            row_height = self.height / self.rows
            # номер удаляемого прямоугольника вычисляется как координаты нажатия
            # по х делить на ширину и по у делить на высоту
            col = int(touch.x // col_width)
            row = int(touch.y // row_height)
            index = row * self.cols + col
            # Удаляем этот прямоугольник
            try:
                self.canvas.remove(self.rectangles[index])
            except:
                print("already clear")


# Главное меню игры
class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding=200
        self.spacing=20

        self.bg = Widget()
        # Это типа создание кнопок
        self.play_button = Button(text='Играть', width=400)
        self.exit_button = Button(text='Выход', width=400)
        # Здесь мы привязываем нажатия кнопок к функциям
        self.settings_button = Button(text='Настройки', width=400)
        self.play_button.bind(on_press=self.start_game)
        self.settings_button.bind(on_press=self.open_settings)
        self.exit_button.bind(on_press=self.exit_game)
        # А здесь добавляем эти кнопки в приложение
        self.add_widget(self.play_button)
        self.add_widget(self.settings_button)
        self.add_widget(self.exit_button)

# Это то что происходит когда нажимаем на кнопку "играть"
    def start_game(self, instance):
        self.clear_widgets()
        popup_content = BoxLayout(orientation='vertical')

        # Три текстовых поля для ввода имени файла, количества строк и столбцов
        self.file_name_input = TextInput(hint_text='Введите имя файла изображения')
        self.rows_input = TextInput(hint_text='Введите количество строк')
        self.cols_input = TextInput(hint_text='Введите количество столбцов')

        # Кнопка начала игры
        start_button = Button(text='Начать игру')
        start_button.bind(on_press=self.launch_game)

        # Здесь добавляется всё что было описано выше
        popup_content.add_widget(self.file_name_input)
        popup_content.add_widget(self.rows_input)
        popup_content.add_widget(self.cols_input)
        popup_content.add_widget(start_button)

        # Здесь это выводится на экран
        self.popup = Popup(title='Настройки игры', content=popup_content, size_hint=(None, None), size=(400, 400))
        self.popup.open()

# Функция, привязанная к кнопке "Начать игру"
    def launch_game(self, instance):

        # Читаем из окошек имя файла, количество строк и столбцов
        file_name = self.file_name_input.text
        rows = int(self.rows_input.text) if self.rows_input.text.isdigit() else 0
        cols = int(self.cols_input.text) if self.cols_input.text.isdigit() else 0
        # Закрываем окошко с настройками
        self.popup.dismiss()
        if rows > 0 and cols > 0:
            # Очищаем экран от всего
            self.clear_widgets()
            # И открываем нашу интерактивную картинку, передаём имя файла, столбцы и строки
            self.padding=0
            self.spacing=0
            self.add_widget(InteractiveImage(file_name, rows, cols))
        else:
            print("Ошибка: Количество строк и столбцов должно быть больше нуля.")

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
