import math
import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram

window = pyglet.window.Window(800, 600)
pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)

# 축, 수식 및 기타등등 그리기
windowbatch = pyglet.graphics.Batch()
xaxis = pyglet.shapes.Line(0, 300, 800, 300, color=(0, 0, 0, 255), batch=windowbatch)
yaxis = pyglet.shapes.Line(400, 0, 400, 600, color=(0, 0, 0, 255), batch=windowbatch)
x1 = pyglet.shapes.Line(600, 310, 600, 290, color=(0, 0, 0, 255), batch=windowbatch)
y1 = pyglet.shapes.Line(390, 500, 410, 500, color=(0, 0, 0, 255), batch=windowbatch)
x1label = pyglet.text.Label("1", 593, 270, font_size=15, color=(0, 0, 0, 255), batch=windowbatch)
y1label = pyglet.text.Label("1", 370, 493, font_size=15, color=(0, 0, 0, 255), batch=windowbatch)
mu = pyglet.sprite.Sprite(pyglet.image.load("mu.jpg"), 450, 200, batch=windowbatch)
sigma = pyglet.sprite.Sprite(pyglet.image.load("sigma.jpg"),  420, 110, batch=windowbatch)
integral = pyglet.sprite.Sprite(pyglet.image.load("integral.jpg"),  430, 30, batch=windowbatch)
nequal = pyglet.sprite.Sprite(pyglet.image.load("nequal.jpg"),  60, 110, batch=windowbatch)
ntoinf = pyglet.sprite.Sprite(pyglet.image.load("ntoinf.jpg"),  73, 111, batch=windowbatch)
ntoinf.visible = False
sliderbar = pyglet.shapes.Line(100, 200, 100, 420, 2, color=(0, 0, 0, 255), batch=windowbatch)
slidertick1 = pyglet.shapes.Line(90, 200, 110, 200, 2, color=(0, 0, 0, 255), batch=windowbatch)
slidertick2 = pyglet.shapes.Line(90, 400, 110, 400, 2, color=(0, 0, 0, 255), batch=windowbatch)
slidertick3 = pyglet.shapes.Line(90, 420, 110, 420, 2, color=(0, 0, 0, 255), batch=windowbatch)
sliderlabel1 = pyglet.sprite.Sprite(pyglet.image.load("1.jpg"), 60, 188, batch=windowbatch)
sliderlabel2 = pyglet.sprite.Sprite(pyglet.image.load("100.jpg"), 45, 386, batch=windowbatch)
sliderlabel3 = pyglet.sprite.Sprite(pyglet.image.load("inf.jpg"), 55, 412, batch=windowbatch)
sliderimg = pyglet.image.load("slider.png")
sliderimg.anchor_x = 15
sliderimg.anchor_y = 5
slider = pyglet.sprite.Sprite(sliderimg, 100, 210, batch=windowbatch)
nlabel = pyglet.text.Label("5", 130, 122, font_size=15, color=(0, 0, 0, 255), batch=windowbatch)
rectsumlabel = pyglet.text.Label("0.749738597555006", 603, 156, font_size=15, color=(0, 0, 0, 255), batch=windowbatch)

dragging = False
mousestate = pyglet.window.mouse.MouseStateHandler()
window.push_handlers(mousestate)
rects = []
rectsum = 0
###########
n = 5
###########


def f(parameter):
    return -4*math.pow(parameter, 2)+4*parameter


# 셰이더 정의
vert_src = """
#version 330 core
in vec2 position;
in vec4 colors;
out vec4 v_color;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    v_color = colors;
}
"""
frag_src = """
#version 330 core
in vec4 v_color;
out vec4 out_color;
void main() {
    out_color = v_color;
}
"""
program = ShaderProgram(Shader(vert_src, 'vertex'),
                        Shader(frag_src, 'fragment'))

# 곡선 데이터
xs = [i * 0.01 for i in range(0, 101)]
pos, col = [], []

for x in xs:
    pos += [x * 0.5, f(x) / 3 * 2]
    col += [255, 50, 50, 255]

vlist = program.vertex_list(len(xs), pyglet.gl.GL_LINE_STRIP, position=('f', tuple(pos)), colors=('Bn', tuple(col)))


# 사각형 그리기
def drawrects(n):
    global rects
    global rectsum
    for _ in range(1, len(rects)+1):
        rects.pop(0)
    rectsum = 0
    for k in range(1, n+1):
        y = (k - 1) / n
        height = 1 / n
        x = (1 - math.sqrt(1 - y)) / 2
        width = math.sqrt(1 - y)
        rects.append(pyglet.shapes.Rectangle(x * 200 + 400, y * 200 + 300, width * 200, height * 200, (int(y*250), 255, 255), batch=windowbatch))
        rectsum += height * width
    if n == 200:
        rectsum = 2/3


@window.event
def on_draw():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    update()
    windowbatch.draw()
    program.use()
    vlist.draw(pyglet.gl.GL_LINE_STRIP)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global dragging
    if 85 <= x <= 115 and 190 <= y <= 430 and button == pyglet.window.mouse.LEFT:
        dragging = True


@window.event
def on_mouse_release(x, y, button, modifiers):
    global dragging
    if button == pyglet.window.mouse.LEFT:
        dragging = False


def update():
    global mousestate
    global dragging
    global slider
    global n
    global nlabel
    global nequal
    global ntoinf
    global rectsumlabel
    global rectsum
    if dragging:
        if mousestate['y'] <= 200:
            slider.y = 200
            n = 1
        elif 200 <= mousestate['y'] <= 400:
            slider.y = mousestate['y']
            n = int((slider.y - 200) / 2)
            if n == 0:
                n = 1
        elif 400 <= mousestate['y'] < 420:
            slider.y = 400
            n = 100
        else:
            slider.y = 420
            n = 200
    drawrects(n)
    nlabel.text = f"{n}"
    if n == 200:
        nlabel.visible = False
        nequal.visible = False
        ntoinf.visible = True
    else:
        nlabel.visible = True
        nequal.visible = True
        ntoinf.visible = False
    rectsumlabel.text = f"{rectsum:.16f}"


pyglet.app.run(1/60)