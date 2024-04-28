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
from kivy.uix.popup import Popup
from random import random
import cv2

# Глобальная переменная для громкости музыки
volume = 0
effects = 0

rows = 5
cols = 5
# В track передаётся саундтрек. Сделал его глобальным, чтобы музыка играла в любой части меню
track = SoundLoader.load('soundtrack.mp3')
sound = SoundLoader.load('click_sound.mp3')


# Класс интерактивной картинки
class InteractiveImage(Widget):
    def __init__(self, image_path, **kwargs):
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
        h = h // self.rows
        w = w // self.cols
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
                    # Color(random(), random(), random(), 1)  # Прозрачный цвет для секций
                    rect = Rectangle(pos=((self.width / self.cols) * col, (self.height / self.rows) * row),
                                     size=(self.width / self.cols, self.height / self.rows),
                                     source=f'pieces/piece_{self.rows - row - 1}_{col}.jpg')
                    self.rectangles.append(rect)

    # Функция, привязанная к нажатию на экран
    def on_touch_down(self, touch):
        super(InteractiveImage, self).on_touch_down(touch)
        # Проверка того, что нажатие внутри изображения

        # if self.collide_point(*touch.pos):
        # Ширина столбца и высота строки считается как ширина и высота окна делить на их количество
        col_width = Window.size[0] / self.cols
        row_height = Window.size[1] / self.rows
        # номер удаляемого прямоугольника вычисляется как координаты нажатия
        # по х делить на ширину и по y делить на высоту
        col = int(touch.x // col_width)
        row = int(touch.y // row_height)
        index = col * self.rows + row
        # Удаляем этот прямоугольник
        try:
            self.canvas.remove(self.rectangles[index])
        except:
            pass


# Главное меню игры
class MainMenu(BoxLayout):
    sound.volume = effects / 100  # Изначальная громкость эффектов
    track.volume = volume / 100   # Изначальная громкость музыки
    track.loop = True             # Когда музыка закончится, она начнёт играть заново
    track.play()                  # Запуск музыки

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        # Вызов функции главного меню. Туда передаётся 0 по приколу, так как прога требует аргумент
        self.my_image = None
        self.open_menu(0)

    # Функция для звука нажатия на кнопку
    def btn_pressed(self, instance):
        global effects
        global sound
        sound.volume = effects / 100
        sound.play()

    # Функция главного меню
    def open_menu(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Добавление фона
        with self.canvas:
            rect = Rectangle(source='background_image1.jpg', size=Window.size)

        # "Кнопка" для красивой надписи, мол сделано нами
        info_text = Button(text='created by 306Team',
                           background_color=(0, 0, 0, 0),
                           color=(0, 0, 0, 1),
                           font_name="397-font.otf",
                           font_size="14sp")
        # Настройка окружения для красивых кнопок
        self.orientation = 'vertical'
        self.size_hint = (0.35, 0.65)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.37}
        self.spacing = 15

        # Создание кнопок
        play_button = Button(text='Играть',
                             background_color=(0, 220 / 255, 20 / 255, 1),  # Цвет фона кнопки
                             color=(1, 1, 1, 1),  # Цвет текста на кнопке
                             font_name="397-font.otf",  # Шрифт
                             font_size="40sp",  # Размер шрифта
                             background_normal='',  # Эти два параметра нужны для того, чтобы фон
                             background_down='',  # не влиял на цвет кнопки
                             on_press=self.btn_pressed)  # Вызов функции звука нажатия на кнопку
        settings_button = Button(text='Настройки',
                                 background_color=(0, 220 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)
        exit_button = Button(text='Выход',
                             background_color=(1, 40 / 255, 50 / 255, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)
        # Пустая кнопка, чтобы сделать отступ для text_info
        empty_button = Button(background_color=(0, 0, 0, 0))

        # Здесь мы привязываем нажатия кнопок к функциям
        play_button.bind(on_press=self.start_game)
        settings_button.bind(on_press=self.open_settings)
        exit_button.bind(on_press=self.exit_game)

        # А здесь добавляем эти кнопки в приложение
        self.add_widget(play_button)
        self.add_widget(settings_button)
        self.add_widget(exit_button)
        self.add_widget(empty_button)
        self.add_widget(info_text)

    # Функция, привязанная к кнопке "Играть"
    def start_game(self, instance):
        global rows, cols

        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Установка новых параметров, чтобы были красивые кнопки
        self.orientation = 'vertical'
        self.size_hint = (0.35, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        rows_layout = BoxLayout(orientation='horizontal',
                                size_hint=(1, 0.6))
        cols_layout = BoxLayout(orientation='horizontal',
                                size_hint=(1, 0.6))

        # Кнопка перехода в меню выбора изображения
        file_name = Button(text='Выбрать файл',
                           background_color=(0, 220 / 255, 20 / 255, 1),
                           color=(1, 1, 1, 1),
                           font_name="397-font.otf",
                           font_size="40sp",
                           background_normal='',
                           background_down='')
        # "Кнопка", в которую передаётся значение количества строк
        rows_input = Button(text=f'Строки: {rows}',
                            background_color=(0, 1 / 4, 1, 1),
                            color=(1, 1, 1, 1),
                            font_name="397-font.otf",
                            font_size="28sp",
                            background_normal='',
                            background_down='')
        # Ползунок для строк
        slider_rows = Slider(min=1, max=10, value=rows,  # Минимальное, максимальное и изначальное значения
                             background_width="30sp",  # Ширина полоски
                             value_track=True,  # Нужно для отслеживания ползунка
                             value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                             cursor_size=(50, 40),  # Размер курсора ползунка
                             cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                             step=1)  # Шаг от 1 до 10 только по целым числам
        slider_rows.bind(value=self.update_value_row)
        # "Кнопка", в которую передаётся значение количества столбцов
        cols_input = Button(text=f'Столбцы: {cols}',
                            background_color=(0, 1 / 4, 1, 1),
                            color=(1, 1, 1, 1),
                            font_name="397-font.otf",
                            font_size="28sp",
                            background_normal='',
                            background_down='')
        # Ползунок для столбцов
        slider_cols = Slider(min=1, max=10, value=cols,
                             background_width="30sp",
                             value_track=True,
                             value_track_color=[1, 1 / 2, 0, 1],
                             cursor_size=(50, 40),
                             cursor_image="cursor.png",
                             step=1)
        slider_cols.bind(value=self.update_value_col)

        # Кнопка начала игры
        start_button = Button(text='Начать игру',
                              background_color=(0, 220 / 255, 20 / 255, 1),
                              color=(1, 1, 1, 1),
                              font_name="397-font.otf",
                              font_size="40sp",
                              background_normal='',
                              background_down='',
                              on_press=self.btn_pressed)
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        # Здесь мы привязываем нажатия кнопок к функциям
        file_name.bind(on_press=self.select_image)
        start_button.bind(on_press=self.launch_game)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        rows_layout.add_widget(rows_input)
        rows_layout.add_widget(slider_rows)
        cols_layout.add_widget(cols_input)
        cols_layout.add_widget(slider_cols)

        self.add_widget(start_button)
        self.add_widget(file_name)
        self.add_widget(rows_layout)
        self.add_widget(cols_layout)
        self.add_widget(exit_button)

    # Функция для изменения значения строк
    def update_value_row(self, instance, value):
        global rows
        label = instance.parent.children[1]  # Получаем Label
        rows = int(value)
        label.text = f'Строки: {rows}'

    # Функция для изменения значения столбцов
    def update_value_col(self, instance, value):
        global cols
        label = instance.parent.children[1]  # Получаем Label
        cols = int(value)
        label.text = f'Столбцы: {cols}'

    # Переменная obj - это filechooser; val - массив с выбранными файлами.
    # Выбираем val[0], так как это первый выбранный пользователем файл
    def selected(self, obj, val):
        try:
            self.my_image.source = val[0]
        except:
            pass

    # Функция для выбора изображения
    def select_image(self, instance):
        # Очищаем экран от всего
        self.clear_widgets()

        # Задаём размеры и позицию виджетов
        # BoxLayout - это структура, которая может в себе содержать несколько кнопок/изображений/ползунков и тд.
        # Мы задаём здесь 2 BoxLayout'а, так как нельзя в одной структуре иметь как горизонтальные,
        # так и вертикальные объекты.
        hbox = BoxLayout(orientation="horizontal",
                         size_hint=(2.5, 0.3),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        vbox = BoxLayout(orientation="vertical",
                         size_hint=(1, 0.085),
                         pos_hint={'center_x': 0.5, 'center_y': 0.1})

        # Добавление виджетов
        self.my_image = Image(fit_mode="scale-down")
        filechooser = FileChooserIconView(filters=["*.jpg", "*.png"],  # Фильтр файлов
                                          font_name='397-font.otf')  # Шрифт
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        filechooser.bind(selection=self.selected)
        exit_button.bind(on_press=self.start_game)

        hbox.add_widget(self.my_image)
        hbox.add_widget(filechooser)
        vbox.add_widget(exit_button)

        self.add_widget(hbox)
        self.add_widget(vbox)

    # Функция, привязанная к кнопке "Начать игру"
    def launch_game(self, instance):
        if self.my_image is None:
            exit_button = Button(text='Назад',
                                 background_color=(1, 1 / 2, 0, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)
            popup = Popup(size_hint=(0.4, 0.25),
                          content=exit_button,
                          title='Ошибка! Выберите файл',
                          title_color=(1, 1, 1, 1),
                          title_font='397-font.otf',
                          title_size='28sp',
                          separator_color=(0, 0, 0, 0))
            popup.open()
            exit_button.bind(on_press=lambda *args: popup.dismiss())
        else:
            # Очищаем экран от всего
            self.clear_widgets()
            self.spacing = 0
            # И открываем нашу интерактивную картинку, передаём имя файла, столбцы и строки
            self.add_widget(InteractiveImage(self.my_image.source))

    # Функция для отображения настроек
    def open_settings(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()
        self.orientation = 'vertical'

        # Установка новых параметров, чтобы были красивые кнопки
        self.size_hint = (0.35, 0.4)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # "Кнопка", в которую передаётся значение количества строк

        music_layout = BoxLayout(orientation='horizontal')
        effects_layout = BoxLayout(orientation='horizontal')

        music_button = Button(text=f'Музыка: {volume}%',
                              background_color=(0, 1 / 4, 1, 1),
                              color=(1, 1, 1, 1),
                              font_name="397-font.otf",
                              font_size="26sp",
                              background_normal='',
                              background_down='')
        # Ползунок для строк
        slider_music = Slider(min=0, max=100, value=volume,  # Минимальное, максимальное и текущее значения
                              background_width="30sp",  # Ширина полоски
                              value_track=True,  # Нужно для отслеживания ползунка
                              value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                              cursor_size=(50, 40),  # Размер курсора ползунка
                              cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                              step=1)  # Шаг от 1 до 100 только по целым числам

        effects_button = Button(text=f'Эффекты: {effects}%',
                                background_color=(0, 1 / 4, 1, 1),
                                color=(1, 1, 1, 1),
                                font_name="397-font.otf",
                                font_size="26sp",
                                background_normal='',
                                background_down='')
        slider_effects = Slider(min=0, max=100, value=effects,
                                background_width="30sp",
                                value_track=True,
                                value_track_color=[1, 1 / 2, 0, 1],
                                cursor_size=(50, 40),
                                cursor_image="cursor.png",
                                step=1)
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        # Здесь мы привязываем нажатия кнопок/ползунков к функциям
        slider_music.bind(value=self.update_value_volume)
        slider_effects.bind(value=self.update_value_volume_effects)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        music_layout.add_widget(music_button)
        music_layout.add_widget(slider_music)
        effects_layout.add_widget(effects_button)
        effects_layout.add_widget(slider_effects)

        self.add_widget(music_layout)
        self.add_widget(effects_layout)
        self.add_widget(exit_button)

    # Функция для изменения значения громкости музыки
    def update_value_volume(self, instance, value):
        global volume
        label = instance.parent.children[1]  # Получаем Label
        volume = int(value)
        track.volume = volume / 100
        label.text = f'Музыка: {volume}%'

    # Функция для изменения значения громкости эффектов
    def update_value_volume_effects(self, instance, value):
        global effects
        label = instance.parent.children[1]  # Получаем Label
        effects = int(value)
        sound.volume = effects / 100
        label.text = f'Эффекты: {effects}%'

    # Функция выхода из игры
    def exit_game(self, instance):
        App.get_running_app().stop()


class GameApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    GameApp().run()
