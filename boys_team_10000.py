from pico2d import *
import random


# Game object class here

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass

#file:///C:/2DGPsyw/20232DGP/2DGP/Slides/LEC10_%EC%BA%90%EB%A6%AD%ED%84%B0%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20(1).pdf
class Boy:
    #클랙스 객체에 항당되는 변수, 객체들은 공유하는 동일한 변수를 갖게 됨 ex(image)
    #클래스변수(Boy).image
    image = None

    #__init__생성자함수 - 객체의 속성의 초기값 생성
    def __init__(self):
        #위치를 나타내는 속성값은 다르다
        self.x, self.y = random.randint(0, 800), 90
        self.frame = random.randint(0,7)

        if Boy.image == None:
            Boy.image = load_image('run_animation.png')

        #같은 이미지를 사용하는 속성이 같다
        #self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running
    global grass
    global team
    global world

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    #boy 랜덤 생성
    team = [Boy() for i in range(10000)]
    world += team


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()
