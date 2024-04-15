from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from PIL import Image

class PaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 1)
            touch.ud['line'] = Line(points=(touch.x, touch.y))


    def on_touch_up(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class PaintApp(App):
    def build(self):
        return PaintWidget()

def flood_fill(image, position, target_color, replacement_color):
    # Получаем данные изображения
    data = image.load()
    width, height = image.size
    target_color = data[position]
    to_fill = set([position])

    while to_fill:
        x, y = to_fill.pop()

        if data[x, y] != target_color or data[x, y] == replacement_color:
            continue

        data[x, y] = replacement_color
        if x > 0:
            to_fill.add((x - 1, y))
        if x < width - 1:
            to_fill.add((x + 1, y))
        if y > 0:
            to_fill.add((x, y - 1))
        if y < height - 1:
            to_fill.add((x, y + 1))

if __name__ == '__main__':
    PaintApp().run()

# Загрузите изображение и используйте функцию flood_fill
image = Image.open('pressed.jpg')
# Замените (0, 0, 0, 0) на цвет, который вы хотите сделать прозрачным
flood_fill(image, (10, 10), (255, 0, 0, 0), (0, 0, 0, 0))
image.save('result_image.png')
