import pygame, sys, time
from settings import *
from random import choice, randint  

StartScreenAT = 'D:\MyGame\BG01.jpg'
Scene2AT = 'D:\MyGame\BG02.jpg'
Scene3AT = 'D:\MyGame\BG03.jpg'
Scene4AT = 'D:\MyGame\BG04.jpg'
Scene5AT = 'D:\MyGame\BG05.jpg'
Scene6AT = 'D:\MyGame\BG06.jpg'
Scene7AT = 'D:\MyGame\BG07.jpg'
Scene8AT = 'D:\MyGame\BG08.jpg'

FontAT = 'D:\MyGame\BD_Cartoon_Shout.ttf'
MusicAT = 'D:\MyGame\ForestWalk.wav'
#MainC = main character
MainCAT = 'D:\MyGame\MainCha-removebg.png'
StepSoundAT = 'D:\MyGame\step_sound.wav'
BirdAT = 'D:\MyGame\BirdObs.png'
ShadowAT = 'D:\MyGame\shadow-removebg.png'

def inverted(img):
		inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
		inv.fill((255,255,255))
		inv.blit(img, (0,0), None, pygame.BLEND_RGB_SUB)
		return inv

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Traveller')
		self.clock = pygame.time.Clock()
		self.active = False

		#self.display_surface.fill((255, 255, 255))

		pixels = pygame.surfarray.pixels2d(self.display_surface)
		pixels ^= 2 ** 32 - 1
		del pixels

		pygame.display.flip()

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
		self.menu_surf = Game.get_font(35).render("-Start Travelling-", True, "#cc6600")
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,(WINDOW_HEIGHT / 2) + (WINDOW_HEIGHT * 0.33)))

		#text
		self.font = pygame.font.Font(FontAT,28)

		#เงาใต้เท้าเด็ก
		global shadow_image
		shadow_image = pygame.image.load(ShadowAT).convert_alpha()

		#ตัวละครหลัก
		global MC_image
		MC_image = pygame.image.load(MainCAT).convert_alpha()

		#ตำแหน่งเงา
		global full_sized_shadow
		full_sized_shadow = pygame.transform.scale(shadow_image,(WINDOW_WIDTH / 15, WINDOW_HEIGHT / 26))
		global sha_rect
		sha_rect = full_sized_shadow.get_rect(midtop = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 1.342))

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

			##     มาแก้ตรงนี้หลังจากได้ฉากมาแล้ว
			posi.y = -16437

	def score_count():
		global score
		score += 1

	def display_score(self):
		if self.active:
			self.score = score
			y = WINDOW_HEIGHT / 1.3
			score_surf = self.font.render(str(self.score) + " m",True,"#ccffff")
			score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2 + 5,y))
		else:
			y = WINDOW_HEIGHT / 10
			x = WINDOW_WIDTH / 2
			score_surf = self.font.render("You have travelled :  " + str(self.score) + " m",True,"#ffffff")
			score_rect = score_surf.get_rect(midtop = (x,y))

		self.display_surface.blit(score_surf,score_rect)
		#self.display_surface.blit(full_sized_shadow,sha_rect)

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
					self.display_surface.blit(full_sized_shadow,sha_rect)
					self.collisions()
			else:
					self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
		


class BG(pygame.sprite.Sprite):

	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		bg_image = pygame.image.load(StartScreenAT).convert()
		bg2_image = pygame.image.load(Scene2AT).convert()
		bg3_image = pygame.image.load(Scene3AT).convert()
		bg4_image = pygame.image.load(Scene4AT).convert()
		bg5_image = pygame.image.load(Scene5AT).convert()
		bg6_image = pygame.image.load(Scene6AT).convert()
		bg7_image = pygame.image.load(Scene7AT).convert()
		bg8_image = pygame.image.load(Scene8AT).convert()
		
        #ความกว้าง/สูงที่พอดีหน้าจอ
		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor

		#สร้างให้เป็น global
		global Gfull_height
		Gfull_height = full_height
		
        #Ready to use
		full_sized_image1 = pygame.transform.scale(bg_image,(full_width,full_height))
		full_sized_image2 = pygame.transform.scale(bg2_image,(full_width,full_height))
		full_sized_image3 = pygame.transform.scale(bg3_image,(full_width,full_height))
		full_sized_image4 = pygame.transform.scale(bg4_image,(full_width,full_height))
		full_sized_image5 = pygame.transform.scale(bg5_image,(full_width,full_height))
		full_sized_image6 = pygame.transform.scale(bg6_image,(full_width,full_height))
		full_sized_image7 = pygame.transform.scale(bg7_image,(full_width,full_height))
		full_sized_image8 = pygame.transform.scale(bg8_image,(full_width,full_height))

		#print(bg_image.get_colorkey)
		
		self.image = pygame.Surface((full_width ,full_height * 8))

		self.image.blit(full_sized_image8,(0,0))
		self.image.blit(full_sized_image7,(0,full_height))
		self.image.blit(full_sized_image6,(0,full_height * 2))
		self.image.blit(full_sized_image5,(0,full_height * 3))
		self.image.blit(full_sized_image4,(0,full_height * 4))
		self.image.blit(full_sized_image3,(0,full_height * 5))
		self.image.blit(full_sized_image2,(0,full_height * 6))
		self.image.blit(full_sized_image1,(0,full_height * 7))

		self.rect_sha = self.image.get_rect(midleft = (full_width / 2.34,-full_height))

		##     มาแก้ตรงนี้หลังจากได้ฉากมาแล้ว
		self.rect = self.image.get_rect(topleft = (0,-full_height * 7.6))

		global posi
		posi = pygame.math.Vector2(self.rect.topleft)
		
		global sha_posi
		sha_posi = pygame.math.Vector2(self.rect_sha.midleft)

		#self.rect.y = -full_height * 1.6

	def move():
		#Obstacle.Birddrop()
		sha_posi.y -= 120
		posi.y += 120

	def update(self,dt, down):
		posi.y += 0 * dt
		#if self.rect.centerx <= 0:
		#	self.pos.x = 0
		self.rect.y = round(posi.y)

class Plane(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):

		super().__init__(groups)

		full_height = MC_image.get_height() * 0.38
		full_width = MC_image.get_width() * 0.38

		RTUMC_image = pygame.transform.scale(MC_image,(full_width * 1.25,full_height * 1.25))

		# image 
		self.image = RTUMC_image

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 2.38,WINDOW_HEIGHT / 7))
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
		if self.rect.bottom > 652:
			self.rect.bottom = 652
			self.direction = 0
			self.gravity = 0
		else:
			self.gravity = 600

	def jump(self):
		self.jump_sound.play()
		self.direction = -200

	def update(self,dt, down):
		self.apply_gravity(dt)


class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'
		
		global surf
		surf = pygame.image.load(BirdAT).convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor * 0.6)

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