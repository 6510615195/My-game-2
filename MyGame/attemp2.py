import pygame
from sys import exit
from random import randint, choice
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk = pygame.image.load('D:\MyGame\GoGo-removebg-preview (1).png').convert_alpha()
		self.player_index = 0

		self.image = player_walk
		self.player_walk2 = pygame.image.load('D:\MyGame\GoGo-removebg-preview (1).png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			#self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_walk2
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk2):self.player_index = 0
			self.image = self.player_walk2

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Traveller')
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

ground_surface = pygame.image.load('D:\MyGame\StartScreen.jpg').convert()

# Intro screen
player_stand = pygame.image.load('D:\MyGame\GoGo-removebg-preview (1).png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))


# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if not(game_active):
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:

		screen.blit(ground_surface,(0,300))

		
		player.draw(screen)
		player.update()

		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)


	pygame.display.update()
	clock.tick(60)