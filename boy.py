# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import (load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, get_time,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_a)
import math
import random


# ----------------------------------------------------------------------------------------
# define event check functions
# ----------------------------------------------------------------------------------------
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def key_a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

# ----------------------------------------------------------------------------------------
# ----------------------Idle--------------------------------------------------------------
# -----------------------------------------------------------------------------------------
class Idle:
    @staticmethod  # 함수 그립핑 class
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0

        boy.idle_start_time = get_time()  # from pico2d import get_time 필요, 현재 경과시간
        print('Idle Enter - 고개 숙이기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.idle_start_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('Idle Do - 드르렁')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit - 고개 들기')
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)


# -----------------------------------------------------------------------------------------
# ----------------------Sleep--------------------------------------------------------------
# -----------------------------------------------------------------------------------------
class Sleep:
    @staticmethod
    def enter(boy, e):
        boy.action = 0
        print('Sleep Enter')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('Sleep')

    @staticmethod
    def exit(boy, e):
        print('Sleep Exit')
        pass

    @staticmethod
    def draw(boy):
        if boy.action == 2:  # 왼쪽방향
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          -math.pi / 2, '', boy.x + 25, boy.y - 30, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          math.pi / 2, '', boy.x - 25, boy.y - 30, 100, 100)


# -----------------------------------------------------------------------------------------
# ----------------------Run----------------------------------------------------------------
# -----------------------------------------------------------------------------------------
class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
        print('Run Enter ')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        print('Run ')

    @staticmethod
    def exit(boy, e):
        print('Run Exit')
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)
# ---------------------------------------------------------------------------------------------
# ----------------------AutoRun----------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.dir, boy.action = random.choice([-1, 1]), 1
        boy.auto_run_start_time = get_time()
        boy.auto_run_end_time = boy.auto_run_start_time + 5
        print('AutoRun Enter')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 7
        if get_time() >= boy.auto_run_end_time:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        if(boy.x > 780):
            boy.dir *= -1
        elif(boy.x < 20):
            boy.dir *= -1
        print('AutoRun')

    @staticmethod
    def exit(boy, e):
        print('AutoRun Exit')
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y + 20,200,200)


# ----------------------------------------------------------------------------------------
# ----------------------StateMachine------------------------------------------------------
# -----------------------------------------------------------------------------------------
class StateMachine:
    def __init__(self, boy):  # self 는 스태이트 머신 self,boy가 첫번째 인자 self가아님
        self.boy = boy
        self.cur_state = Idle  # 지금 상태
        self.transitions = {  # 딕션어리 키로부터 value를 찾는다
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},  # Sleep 상태일 때
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Sleep, key_a_down: AutoRun},  # Idle 상태일 때
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},  # Run 상태일때
            AutoRun: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0)) #어떤 상태인가를 받아오려고

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():  # key = self.cur_state
            if check_event(e):
                self.cur_state.exit(self.boy, e)  # 현재 상태를 나오고
                self.cur_state = next_state  # 다음 상태로 들어가고
                self.cur_state.enter(self.boy, e)  # 다음상태의 행동실행
                return True  # 다음 디버깅 편하라고
        return False

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


# ----------------------------------------------------------------------------------------
# ---------------------- Boy--------------------------------------------------------------
# -----------------------------------------------------------------------------------------
class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)  # 소년의 self = boy다
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
