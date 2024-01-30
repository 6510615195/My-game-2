import pygame, sys, time
from settings import *
from random import choice, randint

StartScreenAT = 'D:\MyGame\StartScreen.jpg'
Scene2AT = 'D:\MyGame\Screen2.jpg'
FontAT = 'D:\MyGame\BD_Cartoon_Shout.ttf'
MusicAT = 'D:\MyGame\ForestWalk.wav'
#MainC = main character
MainCAT = 'D:\MyGame\Traveller-removebg.png'
StepSoundAT = 'D:\MyGame\step_sound.wav'
BirdAT = 'D:\MyGame\FlyingBird-removebg.png'

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Traveller')
		self.clock = pygame.time.Clock()
		self.active = False

		#score
		self.score = 0
		global score
		score = 0
		
        # sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		
        # scale factor
		bg_width = pygame.image.load(StartScreenAT).get_width()
		self.scale_factor = WINDOW_WIDTH / bg_width

		#MAKE IT GLOBAL
		global scale_factor
		scale_factor = self.scale_factor

		#menu
		self.menu_surf = Game.get_font(35).render("-Start Travelling-", True, "#ff6666")
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,(WINDOW_HEIGHT / 2) + (WINDOW_HEIGHT * 0.33)))

		#text
		self.font = pygame.font.Font(FontAT,28)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer, randint(3000, 9000))
		
        # sprite setup 
		BG(self.all_sprites,self.scale_factor)
		#Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)

		#music
		self.music = pygame.mixer.Sound(MusicAT)
		self.music.play(loops = -1)

		self.music.set_volume(20)

	def collisions(self):
	#เมื่อเกิดการชน
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask):
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.plane.kill()
			global score
			score = 0
			self.active = False
			posi.y = -3462

	def score_count():
		global score
		score += 1

	def display_score(self):
		if self.active:
			self.score = score
			y = WINDOW_HEIGHT / 1.3
			score_surf = self.font.render(str(self.score) + " m",True,"#669933")
			score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2 - 16,y))
		else:
			y = WINDOW_HEIGHT / 10
			x = WINDOW_WIDTH / 2
			score_surf = self.font.render("You have travelled :  " + str(self.score) + " m",True,"#ff9933")
			score_rect = score_surf.get_rect(midtop = (x,y))

		self.display_surface.blit(score_surf,score_rect)

	def get_font(size): # Returns Press-Start-2P in the desired size
		return pygame.font.Font(FontAT, size)

			
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
							Game.score_count()
							self.all_sprites.update(dt, down = 1)
							BG.move()
						else:
							self.plane = Plane(self.all_sprites,self.scale_factor / 3)
							self.active = True
							self.start_offset = pygame.time.get_ticks()

					if event.type == self.obstacle_timer and self.active:
						Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)

			self.display_surface.fill('black')
			self.all_sprites.update(dt, down = 0)
			self.all_sprites.draw(self.display_surface)
			self.display_score()

			if self.active: 
					self.collisions()
			else:
					self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
		


class BG(pygame.sprite.Sprite):

	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load(StartScreenAT).convert()
		bg2_image = pygame.image.load(Scene2AT).convert()
		
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

	def move():
		#Obstacle.Birddrop()
		posi.y += 120

	def update(self,dt, down):
		posi.y += 0 * dt
		#if self.rect.centerx <= 0:
		#	self.pos.x = 0
		self.rect.y = round(posi.y)

class Plane(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):

		super().__init__(groups)

		MC_image = pygame.image.load(MainCAT).convert_alpha()

		full_height = MC_image.get_height() * 0.38
		full_width = MC_image.get_width() * 0.38

		RTUMC_image = pygame.transform.scale(MC_image,(full_width,full_height))

		# image 
		self.image = RTUMC_image

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 2.34,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		#step sound
		self.jump_sound = pygame.mixer.Sound(StepSoundAT)
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

	def update(self,dt, down):
		self.apply_gravity(dt)


class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'
		
		global surf
		surf = pygame.image.load(BirdAT).convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor * 0.32)

		global RTUBird
		RTUBird = self.image

		self.y = (WINDOW_HEIGHT) - randint(300,1000)

		self.x = WINDOW_WIDTH + randint(50,60)
		self.rect = RTUBird.get_rect(midbottom = (self.x,self.y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	#def Birddrop(self):
	#	self.y -= 120

	def update(self,dt, down):
		if down == 1:
			self.y += 120
		self.rect.y = self.y
		self.pos.x -= 300 * dt
		self.rect.x = round(self.pos.x)


if __name__ == '__main__':
	game = Game()
	game.run()