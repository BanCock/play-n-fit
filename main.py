from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.filechooser import FileChooserIconView
from random import random

import cv2

# Глобальная переменная для включения/выключения звуков
# (пока что только для звуков кнопок, может быть потом реализуем звуки нажатия на прямоугольники в картинке)
sound_check = 0
# Глобальная переменная для громкости музыки
volume = 0
# В track передаётся саундтрек. Сделал его глобальным, чтобы музыка играла в любой части меню
track = SoundLoader.load('soundtrack.mp3')


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
        self.img = cv2.imread(self.image_path)
        bl = 200
        self.ksize = (bl, bl)
        self.img = cv2.resize(self.img, Window.size)
        #   cv2.imwrite("resized.jpg", self.img)
        self.img = cv2.blur(self.img, self.ksize, cv2.BORDER_DEFAULT)

        h, w, _ = self.img.shape
        h = h // (self.rows)
        w = w // (self.cols)
        for j in range(self.cols):
            for i in range(self.rows):
                piece = self.img[i * h:(i + 1) * h, j * w:(j + 1) * w]
                cv2.imwrite(f'pieces/piece_{i}_{j}.jpg', piece)

        with self.canvas:
            self.bg = Rectangle(source=self.image_path, pos=self.pos, size=Window.size)
            self.size = Window.size

    # Функция отрисовки прямоугольников
    def draw_rectangles(self):
        with self.canvas:
            for col in range(self.cols):
                for row in range(self.rows):
                    #Color(random(), random(), random(), 1)  # Прозрачный цвет для секций
                    rect = Rectangle(pos=((self.width / self.cols) * col, (self.height / self.rows) * row),
                                     size=(self.width / self.cols, self.height / self.rows),
                                     source=f'pieces/piece_{self.rows - row - 1}_{col}.jpg')
                    self.rectangles.append(rect)
            print(self.width, self.height)

    # Функция, привязанная к нажатию на экран
    def on_touch_down(self, touch):
        super(InteractiveImage, self).on_touch_down(touch)
        # Проверка того, что нажатие внутри изображения

        #if self.collide_point(*touch.pos):
        print(touch.pos)
        # Ширина столбца и высота строки считается как ширина и высота окна делить на их количество
        col_width = Window.size[0] / self.cols
        row_height = Window.size[1] / self.rows
        print('col is ', col_width, ' row is ', row_height)
        # номер удаляемого прямоугольника вычисляется как координаты нажатия
        # по х делить на ширину и по y делить на высоту
        col = int(touch.x // col_width)
        row = int(touch.y // row_height)
        print('index col is ', col, ' row is ', row)
        index = col * self.rows + row
        print('index is ', index)
        # Удаляем этот прямоугольник
        try:
            self.canvas.remove(self.rectangles[index])
        except:
            print("already clear")


# Главное меню игры
class MainMenu(BoxLayout):
    track.volume = volume / 100  # Изначальная громкость
    track.loop = True  # Когда музыка закончится, она начнёт играть заново
    track.play()  # Запуск музыки

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        # Вызов функции главного меню. Туда передаётся 0 по приколу, так как прога требует аргумент
        self.open_menu(0)

    # Функция для звука нажатия на кнопку
    def btn_pressed(self, instance):
        global sound_check
        if sound_check == 1:
            sound = SoundLoader.load('click_sound.mp3')
            sound.play()

    # Функция главного меню
    def open_menu(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Добавление фона
        with self.canvas:
            self.rect = Rectangle(source='background_image1.jpg', size=Window.size)
            #print(self.rect.size, Window.size, self.size)

        # "Кнопка" для красивой надписи, мол сделано нами
        info_text = Button(text='created by 306Team',
                           background_color=(0, 0, 0, 0),
                           color=(0, 0, 0, 1),
                           font_name="397-font.otf",
                           font_size="14sp")
        # Настройка окружения для красивых кнопок
        self.orientation = 'vertical'
        self.size_hint = (0.25, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        self.spacing = 15

        # Создание кнопок
        self.play_button = Button(text='Играть',
                                  background_color=(0, 220 / 255, 20 / 255, 1),  # Цвет фона кнопки
                                  color=(1, 1, 1, 1),  # Цвет текста на кнопке
                                  font_name="397-font.otf",  # Шрифт
                                  font_size="36sp",  # Размер шрифта
                                  background_normal='',  # Эти два параметра нужны для того, чтобы фон
                                  background_down='',  # не влиял на цвет кнопки
                                  on_press=self.btn_pressed)  # Вызов функции звука нажатия на кнопку
        self.settings_button = Button(text='Настройки',
                                      background_color=(0, 220 / 255, 20 / 255, 1),
                                      color=(1, 1, 1, 1),
                                      font_name="397-font.otf",
                                      font_size="36sp",
                                      background_normal='',
                                      background_down='',
                                      on_press=self.btn_pressed)
        self.exit_button = Button(text='Выход',
                                  background_color=(1, 40 / 255, 50 / 255, 1),
                                  color=(1, 1, 1, 1),
                                  font_name="397-font.otf",
                                  font_size="36sp",
                                  background_normal='',
                                  background_down='',
                                  on_press=self.btn_pressed)
        # Пустая кнопка, чтобы сделать отступ для text_info
        empty_button = Button(background_color=(0, 0, 0, 0))

        # Здесь мы привязываем нажатия кнопок к функциям
        self.play_button.bind(on_press=self.start_game)
        self.settings_button.bind(on_press=self.open_settings)
        self.exit_button.bind(on_press=self.exit_game)

        # А здесь добавляем эти кнопки в приложение
        self.add_widget(self.play_button)
        self.add_widget(self.settings_button)
        self.add_widget(self.exit_button)
        self.add_widget(empty_button)
        self.add_widget(info_text)

    # Функция, привязанная к кнопке "Играть"
    def start_game(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Установка новых параметров, чтобы были красивые кнопки
        self.size_hint = (0.25, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Текстовое поле для введения имени файла изображения
        # self.file_name_input = TextInput(hint_text='Введите имя файла изображения',  # Изначальный текст
        #                                  background_color=(1 / 2, 1 / 2, 1 / 2, 1),  # Цвет фона поля
        #                                  font_name="397-font.otf",  # Название шрифта
        #                                  font_size="14sp",  # Размер текста
        #                                  hint_text_color=(1, 1, 1, 1))  # Цвет текста
        self.file_name = Button(text='Выбрать файл',
                                background_color=(0, 220 / 255, 20 / 255, 1),
                                color=(1, 1, 1, 1),
                                font_name="397-font.otf",
                                font_size="32sp",
                                background_normal='',
                                background_down='')
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
        self.slider_rows.bind(value=self.update_value_row)
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
                              background_down='',
                              on_press=self.btn_pressed)
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="36sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        # Здесь мы привязываем нажатия кнопок к функциям
        self.file_name.bind(on_press=self.select_image)
        start_button.bind(on_press=self.launch_game)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        self.add_widget(self.file_name)
        # self.add_widget(self.file_name_input)
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

# ЗДЕСЬ ОБЯЗАТЕЛЬНЫ ЭТИ АРГУМЕНТЫ, SELF ЭТО ПОНЯТНО, OBJ ЭТО САМ FILECHOOSER, VAL ЭТО
# МАССИВ С ВЫБРАННЫМИ ФАЙЛАМИ, ПОЭТОМУ БЕРЁМ VAL[0]
    def selected(self, obj, val):
        try:
            self.my_image.source = val[0]
        except:
            print("aaa")

    def select_image(self, instance):
        self.clear_widgets()
        # self.size_hint = (0.5, 0.3)
        # self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
# ЭТО ТЕСТОВЫЙ КОД, НУЖНО ВСЁ ВЫРОВНЯТЬ И СДЕЛАТЬ КРАСИВЫМ

        self.filechooser = FileChooserIconView(size_hint=(2, 0.4),
                                               pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                               font_name='397-font.otf')
        exit_button = Button(text='Назад',
                             size_hint=(1, 0.06),
                             pos_hint={'center_x': 0.5, 'center_y': 0.1},
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="36sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

# ЭТА КАРТИНКА ОТОБРАЖАЕТ ТЕКУЩИЙ ВЫБОР, НУЖНО ВСЁ ПЕРЕДВИНУТЬ ЧТОБЫ ВЛЕЗАЛО НА ЭКРАН,
# ВОЗМОЖНО ПРИДЁТСЯ РАЗМЕЩАТЬ НАПРИМЕР СПРАВА ПАПКИ А СЛЕВА КАРТИНКУ
# ТАКЖЕ Я ДУМАЮ ЧТО НУЖНО ПЕРЕИМЕНОВАТЬ НЕКОТОРЫЕ ПЕРЕМЕННЫЕ ДЛЯ ЯСНОСТИ КОДА
        self.my_image = Image()
        self.filechooser.bind(selection=self.selected)
        exit_button.bind(on_press=self.start_game)

        self.add_widget(self.my_image)
        self.add_widget(self.filechooser)
        self.add_widget(exit_button)

# ТАКЖЕ ДУМАЮ ЧТО МОЖНО РАСКИДАТЬ КАКИЕ-ТО ЧАСТИ ПО РАЗНЫМ ФАЙЛАМ
# МОЖЕТ БЫТЬ ТАК БУДЕТ УДОБНО, ХЗ

    # Функция, привязанная к кнопке "Начать игру"
    def launch_game(self, instance):
        # Читаем из окошка имя файла
        #file_name = self.file_name_input.text

        # Читаем значения строк и столбцов
        rows = int(self.slider_rows.value)
        cols = int(self.slider_cols.value)

        # Очищаем экран от всего
        self.clear_widgets()
        #self.size_hint = (0.0, 0.0)
        #self.pos_hint = {'center_x': 0.0, 'center_y': 0.0}
        self.spacing = 0
        # И открываем нашу интерактивную картинку, передаём имя файла, столбцы и строки
        self.add_widget(InteractiveImage(self.my_image.source, rows, cols))

    # Функция для отображения настроек
    def open_settings(self, instance):
        global sound_check
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Установка новых параметров, чтобы были красивые кнопки
        self.size_hint = (0.25, 0.45)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Кнопка включения/выключения звуков
        self.sound_button = Button(text='Звуки: вкл',
                                   background_color=(0, 220 / 255, 20 / 255, 1),
                                   color=(1, 1, 1, 1),
                                   font_name="397-font.otf",
                                   font_size="22sp",
                                   background_normal='',
                                   background_down='',
                                   on_press=self.btn_pressed,
                                   on_release=self.change_sound_button)

        # Условная конструкция нужна для того, чтобы запомнить состояние кнопки после выхода из меню "Настройки"
        if sound_check == 1:
            self.sound_button.text = 'Звуки: вкл'
            self.sound_button.background_color = (0, 220 / 255, 20 / 255, 1)
        else:
            self.sound_button.text = 'Звуки: выкл'
            self.sound_button.background_color = (1, 20 / 255, 20 / 255, 1)

        # "Кнопка", в которую передаётся значение количества строк
        self.music_button = Button(text=f'Громкость музыки: {volume}%',
                                   background_color=(0, 1 / 4, 1, 1),
                                   color=(1, 1, 1, 1),
                                   font_name="397-font.otf",
                                   font_size="22sp",
                                   background_normal='',
                                   background_down='')
        # Ползунок для строк
        self.slider_volume = Slider(min=0, max=100, value=volume,  # Минимальное, максимальное и текущее значения
                                    background_width="30sp",  # Ширина полоски
                                    value_track=True,  # Нужно для отслеживания ползунка
                                    value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                                    cursor_size=(50, 40),  # Размер курсора ползунка
                                    cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                                    step=1)  # Шаг от 1 до 100 только по целым числам
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="36sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        # Здесь мы привязываем нажатия кнопок/ползунков к функциям
        self.slider_volume.bind(value=self.update_value_volume)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        self.add_widget(self.sound_button)
        self.add_widget(self.music_button)
        self.add_widget(self.slider_volume)
        self.add_widget(exit_button)

    # Функция для изменения значения громкости
    def update_value_volume(self, instance, value):
        global volume
        label = instance.parent.children[2]  # Получаем Label
        volume = int(value)
        track.volume = volume / 100
        label.text = f'Громкость музыки: {volume}%'

    # Функция для изменения кнопки "Включить/Выключить звук"
    def change_sound_button(self, instance):
        global sound_check
        if sound_check == 1:
            instance.text = 'Звуки: выкл'
            instance.background_color = (1, 20 / 255, 20 / 255, 1)
            sound_check = 0
        else:
            instance.text = 'Звуки: вкл'
            instance.background_color = (0, 220 / 255, 20 / 255, 1)
            sound_check = 1

    # Функция выхода из игры
    def exit_game(self, instance):
        App.get_running_app().stop()


class GameApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    print(Window.size)
    GameApp().run()
