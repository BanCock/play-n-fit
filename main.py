from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from random import random


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
                    Color(random(), random(), random(), 1)  # Прозрачный цвет для секций
                    rect = Rectangle(pos=((self.width / self.cols) * col, (self.height / self.rows) * row),
                                     size=(self.width / self.cols, self.height / self.rows))
                    self.rectangles.append(rect)
            print(self.width, self.height)

    # Функция, привязанная к нажатию на экран
    def on_touch_down(self, touch):
        super(InteractiveImage, self).on_touch_down(touch)
        # Проверка того, что нажатие внутри изображения
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
        # Вызов функции главного меню. Туда передаётся 0 по приколу, так как прога требует аргумент
        self.open_menu(0)

    # Функция главного меню
    def open_menu(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Добавление фона
        with self.canvas:
            self.rect = Rectangle(source=f'background_image1.jpg', size=(1920, 1080))

        # "Кнопка" для красивой надписи, мол сделано нами
        self.info_text = Button(text='created by 306Team',
                                background_color=(0, 0, 0, 0),
                                color=(0, 0, 0, 1),
                                font_name="397-font.otf",
                                font_size="14sp")
        # Настройка окружения для красивых кнопок
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (500, 700)
        self.pos = (710, 30)
        self.spacing = 15

        # Создание кнопок
        self.play_button = Button(text='Играть',
                                  background_color=(0, 220 / 255, 20 / 255, 1),  # Цвет фона кнопки
                                  color=(1, 1, 1, 1),  # Цвет текста на кнопке
                                  font_name="397-font.otf",  # Шрифт
                                  font_size="36sp",  # Размер шрифта
                                  background_normal='',  # Эти два параметра нужны для того, чтобы фон
                                  background_down='')    # не влиял на цвет кнопки
        self.settings_button = Button(text='Настройки',
                                      background_color=(0, 220 / 255, 20 / 255, 1),
                                      color=(1, 1, 1, 1),
                                      font_name="397-font.otf",
                                      font_size="36sp",
                                      background_normal='',
                                      background_down='')
        self.exit_button = Button(text='Выход',
                                  background_color=(1, 40 / 255, 50 / 255, 1),
                                  color=(1, 1, 1, 1),
                                  font_name="397-font.otf",
                                  font_size="36sp",
                                  background_normal='',
                                  background_down='')

        # Пустая кнопка, чтобы сделать отступ для text_info
        self.empty_button = Button(background_color=(0, 0, 0, 0))

        # Здесь мы привязываем нажатия кнопок к функциям
        self.play_button.bind(on_press=self.start_game)
        self.settings_button.bind(on_press=self.open_settings)
        self.exit_button.bind(on_press=self.exit_game)

        # А здесь добавляем эти кнопки в приложение
        self.add_widget(self.play_button)
        self.add_widget(self.settings_button)
        self.add_widget(self.exit_button)
        self.add_widget(self.empty_button)
        self.add_widget(self.info_text)

    # Функция, привязанная к кнопке "Играть"
    def start_game(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Установка новых параметров, чтобы были красивые кнопки
        self.size = (500, 800)
        self.pos = (710, 150)

        # Текстовое поле для введения имени файла изображения
        self.file_name_input = TextInput(hint_text='Введите имя файла изображения',  # Изначальный текст
                                         background_color=(1 / 2, 1 / 2, 1 / 2, 1),  # Цвет фона поля
                                         font_name="397-font.otf",  # Название шрифта
                                         font_size="14sp",  # Размер текста
                                         hint_text_color=(1, 1, 1, 1))  # Цвет текста
        # "Кнопка", в которую передаётся значение количества строк
        self.rows_input = Button(text='Количество строк: 5',
                                 background_color=(0, 1 / 4, 1, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="22sp",
                                 background_normal='',
                                 background_down='')
        # Ползунок для строк
        self.slider_rows = Slider(min=1, max=10, value=5,  # Минимальное, максимальное и изначальное значения
                                  background_width="30sp",  # Ширина полоски
                                  value_track=True,  # Нужно для отслеживания ползунка
                                  value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                                  cursor_size=(50, 40),  # Размер курсора ползунка
                                  cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                                  step=1)  # Шаг от 1 до 10 только по целым числам
        # "Кнопка", в которую передаётся значение количества столбцов
        self.cols_input = Button(text='Количество столбцов: 5',
                                 background_color=(0, 1 / 4, 1, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="22sp",
                                 background_normal='',
                                 background_down='')
        # Ползунок для столбцов
        self.slider_cols = Slider(min=1, max=10, value=5,
                                  background_width="30sp",
                                  value_track=True,
                                  value_track_color=[1, 1 / 2, 0, 1],
                                  cursor_size=(50, 40),
                                  cursor_image="cursor.png",
                                  step=1)
        self.slider_cols.bind(value=self.update_value_col)

        # Кнопка начала игры
        start_button = Button(text='Начать игру',
                              background_color=(0, 220 / 255, 20 / 255, 1),
                              color=(1, 1, 1, 1),
                              font_name="397-font.otf",
                              font_size="36sp",
                              background_normal='',
                              background_down='')
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="36sp",
                             background_normal='',
                             background_down='')

        # Здесь мы привязываем нажатия кнопок к функциям
        start_button.bind(on_press=self.launch_game)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        self.add_widget(self.file_name_input)
        self.add_widget(self.rows_input)
        self.add_widget(self.slider_rows)
        self.add_widget(self.cols_input)
        self.add_widget(self.slider_cols)
        self.add_widget(start_button)
        self.add_widget(exit_button)

    # Функция для изменения значения строк
    def update_value_row(self, instance, value):
        label = instance.parent.children[5]  # Получаем Label
        label.text = f'Количество строк: {int(value)}'

    # Функция для изменения значения столбцов
    def update_value_col(self, instance, value):
        label = instance.parent.children[3]  # Получаем Label
        label.text = f'Количество столбцов: {int(value)}'

    # Функция, привязанная к кнопке "Начать игру"
    def launch_game(self, instance):
        # Читаем из окошка имя файла
        file_name = self.file_name_input.text

        # Читаем значения строк и столбцов
        rows = int(self.slider_rows.value)
        cols = int(self.slider_cols.value)

        # Очищаем экран от всего
        self.clear_widgets()
        # И открываем нашу интерактивную картинку, передаём имя файла, столбцы и строки
        self.add_widget(InteractiveImage(file_name, rows, cols))

    # Функция для отображения настроек (пока не написана + как будто и нечего туда добавлять)
    def open_settings(self, instance):
        print("Открыть настройки")

    # Функция выхода из игры
    def exit_game(self, instance):
        App.get_running_app().stop()


class GameApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    GameApp().run()
