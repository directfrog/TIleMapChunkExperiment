import pygame
import sys, os, random
from pygame.locals import *
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

def load_map():
	f = open('map.txt')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(row)
		#we append the row to control the y value of each point in the row
	return game_map 

game_map = load_map()

screen_width = 300
screen_height = 200
over_screen = pygame.display.set_mode((600, 400), 0, 32)
screen = pygame.Surface((screen_width, screen_height))

dirt_img = pygame.image.load('dirt.png')
grass_img = pygame.image.load('grass.png')
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (10, 32))

player_rect = pygame.Rect(screen_width/2, 100, 10, 32)


moving_left = False
moving_right = False
vertical_momentum = 0


def get_collisions(player_rect, tile_rects):
	hit_list = []
	for tile in tile_rects:
		if player_rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move_and_collide(player_rect, player_movement, tile_rects, vertical_momentum):
	player_rect.x += player_movement[0]
	hit_list = get_collisions(player_rect, tile_rects)
	for tile in hit_list:
		if player_movement[0] > 0:
			player_rect.right = tile.left 
		if player_movement[0] < 0:
			player_rect.left = tile.right

	player_rect.y += player_movement[1]
	hit_list = get_collisions(player_rect, tile_rects)
	for tile in hit_list:
		if player_movement[0] > 0:
			player_rect.bottom = tile.top
			print('owoh senpaiii')
			vertical_momentum = 0
		if player_movement[0] < 0:
			player_rect.top = tile.bottom  
	return player_rect, vertical_momentum



while True:
	tile_rects = []
	player_movement = [0, 0]

	screen.fill((135, 206, 235))	

	if moving_left == True:
		player_movement[0] -= 2
	if moving_right == True:
		player_movement[0] += 2
	player_movement[1] += vertical_momentum
	vertical_momentum += 0.15

	y = 0
	for row in game_map:
		x = 0
		for tile in row:
			if tile == '1':
				screen.blit(dirt_img, (x*16, y*16))
			if tile == '2':
				screen.blit(grass_img, (x*16, y*16))
			if tile != '0':
				tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
			x += 1
		y += 1

	player_rect, vertical_momentum = move_and_collide(player_rect, player_movement, tile_rects, vertical_momentum)
	screen.blit(player, (player_rect.x, player_rect.y))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_SPACE:
				vertical_momentum = -5
			if event.key == K_a:
				moving_left = True
			if event.key == K_d:
				moving_right = True
		if event.type == KEYUP:
			if event.key == K_a:
				moving_left = False
			if event.key == K_d:
				moving_right = False



	over_screen.blit(pygame.transform.scale(screen,(600,400)),(0,0))
	pygame.display.update()
	clock.tick(60)
