import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
	# screen setup
	pygame.init()
	font = pygame.font.Font(None, 36)
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	
	print("Starting Asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	print()

	# Object of Clock class to help track time and delta time variable
	# to limit the runtime speed of the game
	clock = pygame.time.Clock()
	dt = 0
	
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = updatable
	Shot.containers = (shots, updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroid_field = AsteroidField()
	
	score = 0

	# Game Loop
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
		screen.fill("black")

		updatable.update(dt)

		for asteroid in asteroids:
			if asteroid.check_collision(player):
				print("Game Over!")
				game_over(screen, score, player)
				player, score = reset_game(updatable, drawable, asteroids, shots)

		for asteroid in asteroids:
			for shot in shots:
				if shot.check_collision(asteroid):
					shot.kill() 
					asteroid.split()
					# Keep track of the score
					score += asteroid.getPoints()
				  
		for obj in drawable:
			obj.draw(screen)

		# Render score text
		score_text = font.render(f"Player Score: {score}", True, "white")
		screen.blit(score_text, (10, 10))

		pygame.display.flip()

		# shoud limit to 60 FPS for this project
		dt = clock.tick(60) / 1000


def game_over(screen, score, player):
	screen.fill("black")
	font =  pygame.font.Font(None, 36)	
	game_over_text = font.render("GAME OVER - Press R to Restart or Esc to Quit", True, "white")
	total_score_text = font.render(f"TOTAL SCORE: {score}", True, "white")
	game_over_box =  game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	total_score_box = total_score_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
	screen.blit(game_over_text, game_over_box)
	screen.blit(total_score_text, total_score_box)
	pygame.display.flip()

	# Now wait for user choice
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					print("Exit.")
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_r:
					return False


def reset_game(updatable, drawable, asteroids, shots):
    # Clear the "figures" from the screen
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    # Re-initialize the player and field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    return player, 0  # Return new player and reset score to 0


if __name__ == "__main__":
	main()