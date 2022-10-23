import pygame
from pygame.color import THECOLORS as COLORS
import pygame.freetype


def draw_background(path):
    path = pygame.transform.scale(path, (1500, 1000))
    screen.blit(path, [0, 0])


def draw_tunnel(path1, path2):
    for x in tunnel_list:
        if [x, 'up'] in passlist:
            continue
        path2 = pygame.transform.scale(path2, (100, 300))
        screen.blit(path2, [x, 0])
    for x in tunnel_list:
        if [x, 'down'] in passlist:
            continue
        path1 = pygame.transform.scale(path1, (100, 350))
        screen.blit(path1, [x+100, 600])


def draw_bird(path):
    screen.blit(path, [bird_x, bird_y])


def draw_context(time, food, target):
    txt = font50.render('Scores: '+str(int(time) + food*2 + target*5), True, COLORS['black'])
    x, y = 10, 920
    screen.blit(txt, (x, y))
    return str(int(time) + food + target)


def draw_food(path, list1, num, foodget):
    bird_rect = (bird_x, bird_y, 70, 70)
    j = 0
    for i in range(fnum):
        food_x = tunnel_list[list1[i]]
        food_rect = (food_x + 25, 450, 50, 50)
        if i in foodate:
            continue
        if rect_cover(bird_rect, food_rect, num):
            foodate.append(i)
            j += 1
            num += 1
            foodget += 1
            continue
        path = pygame.transform.scale(path, (50, 50))
        screen.blit(path, [food_x+25, food_y])
    return num, foodget


def draw_bullet(path, x, y):
    path = pygame.transform.scale(path, (50, 15))
    screen.blit(path, [x, y])


def draw_pause():
    s = pygame.Surface(SIZE, pygame.SRCALPHA)
    s.fill((255, 255, 255, 220))
    screen.blit(s, (0, 0))
    txt = font120.render('PAUSE', True, COLORS['darkgray'])
    x, y = 550, 400
    screen.blit(txt, (x, y))


def draw_dead(time, food, target, dead, n1, bird_x, bird_y, init):
    s = pygame.Surface(SIZE, pygame.SRCALPHA)
    s.fill((255, 255, 255, 240))
    screen.blit(s, (0, 0))
    txt = font120.render('YOU DEAD', True, COLORS['black'])
    screen.blit(txt, (450, 300))
    txt = font120.render('YOUR SCORE IS: ' + str(int(time) + 2 * food + 5 * target), True, COLORS['black'])
    screen.blit(txt, (250, 500))
    txt = font50.render('PRESS ANYKEY TO PLAY AGAIN!', True, COLORS['black'])
    screen.blit(txt, (350, 700))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            dead = False
            n1 = True
            bird_x, bird_y = 700, 450
            init = True
    return dead, n1, bird_x, bird_y, init


def draw_enter():
    s = pygame.Surface(SIZE, pygame.SRCALPHA)
    s.fill((255, 255, 255, 220))
    screen.blit(s, (0, 0))
    txt = font120.render('FlippyBird', True, COLORS['darkgray'])
    screen.blit(txt, (550, 400))


def rect_cover(rect1, rect2, up=True):
    # 第一个对象的点位
    left_up1 = (rect1[0], rect1[1])
    left_down1 = (rect1[0], left_up1[1]+rect1[3])
    right_up1 = (left_up1[0]+rect1[2], rect1[1])
    right_down1 = (left_up1[0]+rect1[2], left_up1[1]+rect1[3])
    # 第二个对象的点位
    left_up2 = (rect2[0], rect2[1])
    left_down2 = (rect2[0], left_up2[1]+rect2[3])
    right_up2 = (left_up2[0]+rect2[2], rect2[1])
    right_down2 = (left_up2[0]+rect2[2], left_up2[1]+rect2[3])
    # 检测
    if (left_up2[0] <= right_up1[0] <= right_up2[0]) or (left_up2[0] <= left_up1[0] <= right_up2[0]):
        if (left_up2[1] >= left_up1[1] >= left_down2[1]) or (left_up2[1] >= left_down1[1] >= left_down2[1]):
            return True
        if up and (left_up2[1] <= right_up1[1] <= left_down2[1]):
            return True
        elif (not up) and (left_up2[1] <= right_down1[1] <= left_down2[1]):
            return True
    if (left_up1[0] <= right_up2[0] <= right_up1[0]) or (left_up1[0] <= left_up2[0] <= right_up1[0]):
        if (left_up1[1] >= left_up2[1] >= left_down1[1]) or (left_up1[1] >= left_down2[1] >= left_down1[1]):
            return True
        if up and (left_up1[1] <= right_up2[1] <= left_down1[1]):
            return True
        elif (not up) and (left_up1[1] <= right_down2[1] <= left_down1[1]):
            return True
    return False


def check_dead():
    bird_rect = (bird_x, bird_y, 70, 70)
    if bird_rect[1]+bird_rect[3] > 900:
        return True
    for x in tunnel_list:
            up_rect = (x, 0, 100, 300)
            if [x, 'up'] in passlist:
                continue
            if rect_cover(bird_rect, up_rect):
                return True
    for x in tunnel_list:
        down_rect = (x+100, 600, 100, 350)
        if [x, 'down'] in passlist:
            continue
        if rect_cover(bird_rect, down_rect, up=False):
            return True
    return False


def check_bullet(targetnum):
    bullet_rectlist = []
    for i in range(len(bullet_xlist)):
        bullet_rectlist.append((bullet_xlist[i], bullet_ylist[i], 50, 15))
    for x in tunnel_list:
        if [x, 'up'] in passlist or [x, 'down'] in passlist:
            continue
        up_rect = (x, 0, 100, 300)
        down_rect = (x+100, 600, 100, 350)
        for j in range(len(bullet_rectlist)):
            if rect_cover(bullet_rectlist[j], up_rect):
                passlist.append([x, 'up'])
                bullet_xlist.pop(j)
                bullet_ylist.pop(j)
                targetnum += 1
                break
            if rect_cover(bullet_rectlist[j], down_rect, up=False):
                passlist.append([x, 'down'])
                bullet_xlist.pop(j)
                bullet_ylist.pop(j)
                targetnum += 1
                break
    return targetnum


if __name__ == "__main__":
    # 初始化
    pygame.init()
    
    # 内容
    SIZE = [1500, 1000]
    font50 = pygame.font.SysFont('Times', 50)
    font120 = pygame.font.SysFont('Times', 120)
    G = 9.8*30
    JUMP_V = -300
    GOLD = 255, 251, 0
    WHITE = 255, 255, 255
    YELLOW = 255, 235, 205
    GREEN = 0, 205, 0
    ORANGE = 255, 165, 0

    # 载入图片
    birdPath = pygame.image.load('bird.png')
    foodPath = pygame.image.load('food.png')
    tunnelPath1 = pygame.image.load('tunnel1.png')
    tunnelPath2 = pygame.image.load('tunnel2.png')
    bulletPath = pygame.image.load('bullet.png')
    bankgroundPath = pygame.image.load('bankground.png')

    # 管道出现位置预设
    tunnel_list = [100, 600, 1100, 1600, 2100]

    # 根据SIZE创建屏幕
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("像素鸟")

    # 管道的横向速度以及帧率设置
    data = [(3, 0.02, 4), (5, 0.02, 3), (15, 0.02, 2)]
    speed, frame, fnum = data[1]    # 默认为中等难度

    # 变量初始化
    bird_x, bird_y = 700, 450
    bullet_xlist = []
    bullet_ylist = []
    bird_v = 0
    bullet_v = 1000
    count_time = 0
    foodnum = 0
    bulletnum = 0
    target = 0
    bulletnumpast = bulletnum
    targetnum = 0
    passlist = []
    foodate = []
    flaglist = []

    # 参数准备
    running = True
    pause = False
    jump = False
    dead = False
    fire = False
    init = False
    f1 = pygame.freetype.Font("C://Windows//Fonts//STHUPO.TTF", 36)
    n1 = True
    f1surf, f1rect = f1.render("像素鸟", fgcolor=GREEN, size=100)
    f2surf, f2rect = f1.render("简单", fgcolor=ORANGE, size=50)
    f3surf, f3rect = f1.render("中等", fgcolor=ORANGE, size=50)
    f4surf, f4rect = f1.render("困难", fgcolor=ORANGE, size=50)
    f5surf, f5rect = f1.render("退出游戏", fgcolor=WHITE, size=50)

    # 主循环
    while running:
        bankgroundPath = pygame.transform.scale(bankgroundPath, (1500, 1000))
        screen.blit(bankgroundPath, [0, 0])
        while n1:
            screen.blit(f1surf, (600, 100))
            screen.blit(f2surf, (600, 300))
            screen.blit(f3surf, (600, 400))
            screen.blit(f4surf, (600, 500))
            screen.blit(f5surf, (600, 600))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x1, y1 = pygame.mouse.get_pos()
                    if 600 <= x1 <= 700 and 300 <= y1 <= 400:
                        if event.button == 1:
                            n1 = False
                            speed, frame, fnum = data[0]
                    if 600 <= x1 <= 700 and 400 <= y1 <= 500:
                        if event.button == 1:
                            n1 = False
                            speed, frame, fnum = data[1]
                    if 700 >= x1 >= 600 >= y1 >= 500:
                        if event.button == 1:
                            n1 = False
                            speed, frame, fnum = data[2]
                    if 600 <= x1 <= 800 and 600 <= y1 <= 700:
                        if event.button == 1:
                            n1 = False
                            pygame.quit()
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pause = not pause
            elif event.type == pygame.KEYUP:
                if chr(event.key) == ' ':
                    jump = True
                if chr(event.key) == 'f' and bulletnum > 0:
                    fire = True
                    bullet_xlist.append(bird_x+70)
                    bullet_ylist.append(bird_y+35)
                    fire = False
                    bulletnum -= 1

        # 更新数据
        if not pause and not dead:
            count_time += frame
            for i in range(len(tunnel_list)):
                if tunnel_list[i] - speed > -200:
                    tunnel_list[i] = tunnel_list[i] - speed
                else:
                    tunnel_list[i] = 2100

            poplist = []
            for i in range(len(passlist)):
                if passlist[i][0] - speed > -200:
                    passlist[i][0] = passlist[i][0] - speed
                else:
                    poplist.append(i)

            for i in range(len(poplist)):
                passlist.pop(0)
                poplist.pop(0)

            if not jump:
                bird_v += G*frame
            else:
                bird_v = JUMP_V
                jump = False
            bird_y += frame*bird_v

            food_xlist = [0, 1, 2, 4]
            food_y = 450
            targetnum = check_bullet(targetnum)

        draw_background(bankgroundPath)
        draw_tunnel(tunnelPath1, tunnelPath2)
        if bulletnumpast > bulletnum:
            foodate.pop(-1)
        bulletnum, foodnum = draw_food(foodPath, food_xlist, bulletnum, foodnum)
        bulletnumpast = bulletnum
        draw_bird(birdPath)
        draw_context(count_time, foodnum, targetnum)
        for i in range(len(bullet_xlist)):
            draw_bullet(bulletPath, bullet_xlist[i], bullet_ylist[i])
            bullet_xlist[i] = bullet_v * frame + bullet_xlist[i]

        if not dead and pause:
            draw_pause()

        # 暂停 20ms
        pygame.time.delay(int(frame*1000))

        # 检查是否死亡
        if check_dead():
            dead = True

        # 后事
        if dead:
            dead, n1, bird_x, bird_y, init = draw_dead(count_time, foodnum, targetnum, dead, n1, bird_x, bird_y, init)
            if init == True:
                bird_x, bird_y = 700, 450
                bullet_xlist = []
                bullet_ylist = []
                bird_v = 0
                count_time = 0
                foodnum = 0
                bulletnum = 0
                target = 0
                bulletnumpast = bulletnum
                targetnum = 0
                passlist = []
                foodate = []
                flaglist = []
                init = False

        # 刷新窗口
        pygame.display.update()

    pygame.quit()
