# 버그: 피사체가 사라졌지만 총알은 계속 맞는 버그
# 버그: 피사체가 있는 위치에 총을 쏠 경우 총알의 발사속도가 빨라짐
# 버그: 발사체의 y축 위치에 따라서 총알의 발사속도가 달라짐
# 버그: 발사체가 화면 밖으로 계속 나갈 수 있음.

# pygame 라이브러리를 가져와라.
import pygame
# pygame 라이브러리를 pg 라는 이름으로 가져와라.
import pygame as pg
from pygame.locals import *
from operator import truediv

import Actor

import random
import math
score=0000000

# 컬러 값을 미리 설정한다. 컴퓨터에서 컬러를 표현할때 RGB를 사용한다.
BLACK = (0, 0, 0) # 검정

# 게임창에 텍스트를 출력하기 위한 함수코드
# printText(출력하고싶은 내용, 컬러, 위치)
def printText(msg, color='BLACK', pos=(50,50)):
    font= pygame.font.SysFont("consolas",20)
    textSurface     = font.render(msg,True, pygame.Color(color),None)
    textRect        = textSurface.get_rect()
    textRect.topleft= pos
    screen.blit(textSurface, textRect)


#===========================================파이게임 코딩을 시작하는 부분

# 가장 윗줄에 게임에 대한 값들을 초기화
pygame.init()

# 배경음악을 셋팅
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

# 배경 맵
background = pygame.image.load("background.png")

# 게임 창의 X(가로)의 차원 (길이)
nX = 1010
# 게임 창의 Y(세로)의 차원 (길이) 
nY = 700

# size라는 list 데이터로 가지고 있음
size = [nX, nY]

keyFlag = None

# 게임 창의 크기를 셋팅한다.
# pygame 라이브러리 사용
screen = pygame.display.set_mode(size)
# pygame 라이브러리 사용하여 게임창의 이름을 붙여준다.
pygame.display.set_caption("Mario")

# 시간 시작 tick을 받아옴
start_ticks=pygame.time.get_ticks()

done = False
clock = pygame.time.Clock()

# Actor클래스를 사용하여 객체(주인공) 하나를 생성
hero = Actor.Actor(pygame)
hero.setImage("man.png")
hero.setScale(150, 150)
hero.setPosition(nX/2, nY/2 + 150)
hero.setVitality(100)
hero.estimateCenter()

bullet = Actor.Actor(pygame)
bullet.setImage("bullet.png")
bullet.setScale(20, 20)
bullet.setPosition(hero.centerX, hero.centerY)
bullet.setSound("laser.wav")
bullet.estimateCenter()
bullet.damage(20)

# actor클래스를 사용하여 객체(적) 하나를 더 생성
enermy = Actor.Actor(pygame)
enermy.setImage("tacco.png")
enermy.setScale(180, 180)
enermy.setPosition(nX/2, nY/2 - 350)
enermy.setVitality(500)
enermy.estimateCenter()

# enermy 공격 물체 = 음식 (-Attack.png)
food = Actor.Actor(pygame)
food.setImage("taccoAttack.png")
food.setScale(70, 70)
food.setPosition(nX/2, nY/2 - 350)
food.estimateCenter()

# 힐팩 액터
heal = Actor.Heal(pygame)
heal.setImage("hill.png")
heal.setScale(70, 70)
heal.estimateCenter()

# 파워업 액터
PowerUp = Actor.PowerUp(pygame)
PowerUp.setImage("power.png")
PowerUp.setScale(50,50)
PowerUp.estimateCenter()

# 총알이 날아가고 있는가?
bulletFire = False
# bullet delta 총알이 날아가는 변화량
bd = 0

dx = 0
dy = 0
ds = 0

start_ticks = pygame.time.get_ticks()

heal_flag = True

# 적이 죽은 횟수
cnt = 0

def enemyIsDead(Cnt):
    enermy.setImage("tacco.png")
    enermy.setScale(180, 180)
    enermy.setPosition(nX/2, nY/2-200)
    enermy.setVitality(500*(Cnt+1))
    enermy.estimateCenter()

# 반복자 while문
# done이 False를 유지하는 동안 계속 실행, not False = True
while not done:
    # set on 10 frames per second (FPS)
    clock.tick(50)
    
    # 게임을 실행하는 기능들을 실제로 여기에 구현

    # 스크린의 배경색을 채워넣기
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    
    # 경과시간(ms)을 1000으로 나누어 초 단위로 표시s
    elapsed_timer=(pygame.time.get_ticks()-start_ticks)/1000
    # 초를 분:초로 나타내기 위함
    elapsed_timer_hour=int(elapsed_timer/60)
    # 초를 분:초로 나타내기 위함
    elapsed_timer_sec=int(elapsed_timer%60)
    # 텍스트 함수
    printText(str(elapsed_timer_hour)+":"+str(elapsed_timer_sec), color=(255,255,255), pos=(10,10))

    # score 표시함수
    printText("score:"+str(score),color=(255,255,255),pos=(10,30))
    
    time = (pygame.time.get_ticks() - start_ticks) / 1000
    
    if time % PowerUp.interval < 0.1 and PowerUp.islive == False:
        food.reset(screen)
    
    if food.y > screen.get_width():
        food.islive = False
    
    if food.isAlive:
        food.drop()
        food.drawActor(screen)
        food.estimateCenter()
    
    if time % heal.interval < 0.1 and heal.islive == False:
        heal.reset(screen)

    # 힐팩이 너무 밑으로 내려가면
    if heal.y > screen.get_width():
        heal.islive = False

    if heal.islive:
        heal.drop()
        heal.drawActor(screen)
        heal.estimateCenter()
        # 히어로가 먹은 경우
        if heal.isCollide(hero):
            heal.islive = False
            # 생명력 증가량
            hero.increaseVitality(20)

    if time % PowerUp.interval < 0.1 and PowerUp.islive == False:
        PowerUp.reset(screen)

    # 힐팩이 너무 밑으로 내려가면
    if PowerUp.y > screen.get_width():
        PowerUp.islive = False

    if PowerUp.islive:
        PowerUp.drop()
        PowerUp.drawActor(screen)
        PowerUp.estimateCenter()
        # 히어로가 먹은 경우
        if PowerUp.isCollide(hero):
            PowerUp.islive = False
            # 공격력 증가량
            bullet.damage()+10

    # 어떤 이벤트가 들어왔을때 그 이벤트를 가져옴
    for event in pygame.event.get():

        # 그 특정 이벤트가 무엇인지 직접 확인하는 절차
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                print("왼쪽키 누름")
                dx = - 10
            elif event.key == pygame.K_RIGHT:
                print("오른쪽키 누름")
                dx = 10
            elif event.key == pygame.K_DOWN:
                print("아래키 누름")
                dy = 10
            elif event.key == pygame.K_UP:
                print("위로키 누름")
                dy = -10
            elif event.key == pygame.K_a:
                print("버튼a 누름")
                ds = 3
            elif event.key == pygame.K_SPACE:
                print("스페이스 버튼 누름")

                if bulletFire == False:
                    bullet.soundPlay()
                    hero.estimateCenter()
                    # 총을 쏠때, 총알의 위치를 주인공의 위치로 셋팅
                    bullet.setPosition(hero.centerX, hero.centerY)
                    bd = -20
                    bulletFire = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                print("왼쪽키 떼짐")
                dx = 0
            elif event.key == pygame.K_RIGHT:
                print("오른쪽키 떼짐")
                dx = 0
            elif event.key == pygame.K_DOWN:
                print("아래키 떼짐")
                dy = 0
            elif event.key == pygame.K_UP:
                print("위로키 떼짐")
                dy = 0
            elif event.key == pygame.K_a:
                print("버튼a 누름")
                ds = 0
                
    hero.estimateCenter()
    enermy.estimateCenter()
    food.estimateCenter()
    
    if hero.isCollide(enermy):
        print("적과 충돌함")
        hero.decreaseVitality(0.5)

    if bullet.y < 0:
        bulletFire = False

    # 총을 쏘고 있는가? 이게 참이라면 총알을 계속 이동시켜야 함
    if bulletFire == True:
        
        bullet.move(0, bd)
        bullet.estimateCenter()
        enermy.estimateCenter()
        food.estimateCenter()
        bullet.drawActor(screen)

        collsion = bullet.isCollide(enermy)
        if collsion == True:
            print("부딪힘")
            enermy.decreaseVitality(50)
            bulletFire = False

    hero.move(dx, dy)
    hero.drawActor(screen)
    hero.drawEnergyBar(screen)

    if enermy.isDead == False:
        enermy.drawActor(screen)
        enermy.drawEnergyBar(screen)
        enermy.moveRandomly(nX, nY)

        if hero.isDead == True:
            print("나 죽음")
            pygame.display.update()

    elif enermy.isDead == True:
        cnt += 1
        enemyIsDead(cnt)
        enermy.drawActor(screen)
        enermy.drawEnergyBar(screen)
        enermy.moveRandomly(nX, nY)
        enermy.isDead = False
    
    pygame.display.update()

# 게임을 끝내는 명령어
pygame.quit()