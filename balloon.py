import pygame
from random import randint as ra
from random import choice as ch
import time
import sys

class Balloon:

    def __init__(self):
        pygame.init()
        self.scr = pygame.display.set_mode((800, 800))
        self.bal_ori = pygame.image.load('balloon.png')
        self.bal = pygame.transform.scale(self.bal_ori, (100,80))
        pygame.mixer.init()  # 初始化音频模块
        self.win = False
        self.lose = False
        self.max_num = 5
        self.speed = 0
        self.x = 200
        self.y = 200
        self.clock = pygame.time.Clock()
        self.dps = 60
        self.balloons = []
        self.bfont = pygame.font.Font('msyhbd.ttc', 20)
        self.sfont = pygame.font.Font('msyhbd.ttc', 50)
        self.input_text = ''
        self.explode_sound = pygame.mixer.Sound('explosion.mp3')  # 加载音效文件
        self.error_sound = pygame.mixer.Sound('error.wav')  # 加载音效文件
        pygame.mixer.music.load('bgm.wav')
        self.score = 0
        self.run = True
        self.start_time = time.time()  # 获取游戏开始时间
        self.total_time = 30  # 总倒计时时间（60秒）
        self.bk = (0,0,0)
        self.w = (255,255,255)
        self.re = (255,0,0)
        self.level = '2'
            # '1': '20以内加法',
            # '2': '20以内减法',
            # '3': '20以内混合加减法',
            # '4': '100以内加法',
            # '5': '100以内减法',
            # '6': '100以内混合加减法',
            # '7': '乘法口诀',
            # '8': '英文字母',
        pygame.mixer.music.set_volume(0.5)  # 设置音量为 50%
        pygame.mixer.music.play(-1)

    def 运行游戏(self):
        while True:
            self.响应事件()
            if self.run:
                self.显示气球和内容()
                self.显示得分()
                self.显示倒计时()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.dps)

    def 获取剩余时间(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(self.total_time - elapsed_time, 0)
        return remaining_time
    
    def 显示气球和内容(self):
        self.scr.fill((255,255,255))
        while len(self.balloons) < 3:
            self.生成气球()
        for balloon in self.balloons:
            self.char = self.bfont.render(balloon['char'], True, balloon['text_color'])
            self.scr.blit(self.bal, (balloon['x'], balloon['y']))
            self.scr.blit(self.char, ((balloon['x'] + 25), (balloon['y'] + 16)))
            balloon['y'] -= balloon['speed']
            if balloon['y'] < 50:
                self.balloons.remove(balloon)

    def 生成气球(self):
        
        balloon = {}
        #TODO: 气球最小间距
        balloon['x'] = ra (100,700)
        balloon['y'] = ra (780,900)
        balloon['speed'] = ra (1,2) / 2
        char, answer = self.生成气球文字和答案()
        balloon['char'] = char
        balloon['answer'] = answer 
        balloon['text_color'] = self.bk
        balloon['score'] = balloon['speed']*2
        self.balloons.append(balloon)
        self.char_rect = (balloon['x'], balloon['y'])

    def 响应事件(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and len(self.input_text) < 2:
                    self.input_text += event.unicode
                elif event.key == pygame.K_SPACE and self.run:
                    for balloon in self.balloons:
                        print(self.input_text)
                        print(balloon['answer'])
                        if int(self.input_text) == balloon['answer']:
                            balloon['text_color'] = self.w
                            time.sleep(0.2)
                            self.score += balloon['score']
                            self.balloons.remove(balloon)
                            self.explode_sound.play()
                            break
                    self.error_sound.play()
                    self.input_text = ""


    def 生成气球文字和答案(self):

        while self.level == '1':
            p = ra (1,10)
            q = ra (1,10)
            if p + q < 10:
                continue
            char = f'{p}+{q}'
            answer = int(p + q)
            return char, answer
        
        while self.level  == '2':
            p = ra (9,19)
            q = ra (0,19)
            if p > q:
                char = f'{p}-{q}'
                answer = int(p - q)
            else:
                continue
            return char, answer
        
        while self.level == '3':
            pass

        while self.level == '4':
            p = ra (1, 100)
            q = ra (1, 100)
            if 10 < p + q < 100:
                char = f'{p}+{q}'
                answer = int(p + q)
                return char, answer
            else:
                continue
        
        while self.level  == '5':
            p = ra (20,100)
            q = ra (1,100)
            if p > q:
                char = f'{p}-{q}'
                answer = int(p - q)
            else:
                continue
            return char, answer
        
        while self.level == '6':
            pass
    
        while self.level == '7':
            p = ra (1,9)
            q = ra (1,9)
            char = f'{p}*{q}'
            answer = int(p * q)
            return char, answer

    def 显示得分(self):
        score_text = f'得分：{str(int(self.score))}'
        score = self.sfont.render(score_text, True, self.bk)
        self.scr.blit(score, (20,0))
        if self.score >= 20:
            win_text = f'胜利,你太棒了'
            score = self.sfont.render(win_text, True, self.re)
            self.scr.blit(score, (200,400))
            self.run = False
            

    def 显示倒计时(self):
        time_text = f'剩余时间：{int(self.获取剩余时间())}'
        score = self.sfont.render(time_text, True, self.bk)
        self.scr.blit(score, (430,0))
        if self.获取剩余时间() == 0:
            lose_text = f'时间到了,还要加油哦！'
            score = self.sfont.render(lose_text, True, self.re)
            self.scr.blit(score, (200,400))
            self.run = False
        
if __name__ == '__main__':
    role = Balloon()
    role.运行游戏()
