import pygame, sys, time
from settings import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#ตั้งชื่อเกม
pygame.display.set_caption('Traveller')

#clock ใช้ควบคุม frame rate
clock = pygame.time.Clock()

#font
test_font = pygame.font.Font(None, 50)

StartScreen_surface = pygame.image.load('D:\MyGame\StartScreen.jpg')
Screen2_surface = pygame.image.load('D:\MyGame\Screen2.jpg')

#หา factor
scale_factor = WINDOW_WIDTH / StartScreen_surface.get_width()

#หา ความกว้าง/สูงของรูปที่ต้องการ
full_height = StartScreen_surface.get_height() * scale_factor
full_width = StartScreen_surface.get_width() * scale_factor

#Ready to use
RTUStartScreen_surface = pygame.transform.scale(StartScreen_surface, (full_width,full_height))
RTUSScreen2_surface = pygame.transform.scale(Screen2_surface, (full_width,full_height))

#---------พื้นที่ทดลอง----------

ima = pygame.Surface((WINDOW_WIDTH ,WINDOW_HEIGHT))

rectang = ima.get_rect(topleft = (0,0))
pos = pygame.math.Vector2(rectang.topleft)

pos.y = StartScreen_surface.get_height()

#---------พื้นที่ทดลอง----------

#ใส่สีให้ surface
#test_surface.fill('Cyan')

while True:
    #ตรวจหาevent
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #blit ใช้สั่งให้เอา surface หนึ่ง ไปใส่ในอีก surface หนึ่ง
    screen.blit(RTUSScreen2_surface, (0,0))
    screen.blit(RTUStartScreen_surface, (0, full_height ))

    #draw all elements
    #update everything
    pygame.display.update()

    #รันไม่เกิน 60 รูปใน 1 วินาที(ุ60 fps)
    clock.tick(60)
    