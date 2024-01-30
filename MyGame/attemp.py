import pygame, sys, time
from settings import *
from random import choice, randint

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Traveller')
		self.clock = pygame.time.Clock()
		self.active = True

		#สำหร้บตำแหน่งนกใน obstacle
		global y_position
		y_position = WINDOW_HEIGHT
		
        # sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		
        # scale factor
		bg_width = pygame.image.load('D:\MyGame\StartScreen.jpg').get_width()
		self.scale_factor = WINDOW_WIDTH / bg_width

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer, 1400)

		#MAKE IT GLOBAL
		global scale_factor
		scale_factor = self.scale_factor
		
        # sprite setup 
		BG(self.all_sprites,self.scale_factor)
		self.plane = Plane(self.all_sprites,self.scale_factor / 3)
		Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)

		#music
		self.music = pygame.mixer.Sound('D:\MyGame\ForestWalk.wav')
		self.music.play(loops = -1)

		self.music.set_volume(20)

			
	def run(self):
	
		last_time = time.time()
		while True:

			#แยกเงาพันร่าง
			#Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			#ตรวจหา event
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if self.active:
							self.plane.jump()
							BG.move(self)

					if event.type == self.obstacle_timer and self.active:
						Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)

			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			pygame.display.update()
		


class BG(pygame.sprite.Sprite):

	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load('D:\MyGame\StartScreen.jpg').convert()
		bg2_image = pygame.image.load('D:\MyGame\Screen2.jpg').convert()
		
        #ความกว้าง/สูงที่พอดีหน้าจอ
		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor

		#สร้างให้เป็น global
		global Gfull_height
		Gfull_height = full_height
		
        #Ready to use
		full_sized_image1 = pygame.transform.scale(bg_image,(full_width,full_height))
		full_sized_image2 = pygame.transform.scale(bg2_image,(full_width,full_height))
		
		self.image = pygame.Surface((full_width ,full_height * 8))
		self.image.blit(full_sized_image2,(0,0))
		self.image.blit(full_sized_image1,(0,full_height))

		self.rect = self.image.get_rect(topleft = (0,-full_height * 1.6))

		global posi
		posi = pygame.math.Vector2(self.rect.topleft)

		#self.rect.y = -full_height * 1.6

	def move(self):
		global y_position
		#y_position += 120
		#Obstacle.Birddrop()
		posi.y += 120

	def update(self,dt):
		#posi.y += 0 * dt
		#if self.rect.centerx <= 0:
		#	self.pos.x = 0
		self.rect.y = round(posi.y)

class Plane(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):

		super().__init__(groups)

		MC_image = pygame.image.load('D:\MyGame\Oldman.png').convert_alpha()

		full_height = MC_image.get_height() * 0.19
		full_width = MC_image.get_width() * 0.19

		RTUMC_image = pygame.transform.scale(MC_image,(full_width,full_height))

		# image 
		self.image = RTUMC_image

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 2.37,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		#step sound
		self.jump_sound = pygame.mixer.Sound('D:\MyGame\step_sound.wav')
		self.jump_sound.set_volume(2)


	def apply_gravity(self,dt):
		#self.gravity += 1
		#self.rect.y += self.gravity
		#if self.rect.bottom >= 2000:
		#	self.rect.bottom = 500


		self.direction += self.gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)
		if self.rect.bottom > 620:
			self.rect.bottom = 620
			self.direction = 0
			self.gravity = 0
		else:
			self.gravity = 600

	def jump(self):
		self.jump_sound.play()
		self.direction = -260

	def update(self,dt):
		self.apply_gravity(dt)


class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'
		
		global surf
		surf = pygame.image.load('D:\MyGame\FlyingBird-removebg.png').convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor * 0.2)

		global RTUBird
		RTUBird = self.image

		global y_position
		y_position += -randint(600,1000)

		global x_position
		x_position = WINDOW_WIDTH + randint(50,60)
		self.rect = RTUBird.get_rect(midbottom = (x_position,y_position))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		global Birdposi
		Birdposi = self.pos

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	#def Birddrop():
	#	y_position -= 120

	def update(self,dt):
		print(posi.y)
		self.rect.y = posi.y + 3462
		self.pos.x -= 50 * dt
		self.rect.x = round(self.pos.x)


if __name__ == '__main__':
	game = Game()
	game.run()