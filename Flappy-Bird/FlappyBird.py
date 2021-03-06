import pygame
from pygame.locals import *

from Genetic_Algorithm import Genetic_Algorithm
from Pipe import Pipe

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red_blue = (255, 0, 255)
pipe_color = (117, 194, 26)

height = 600
width = 400


pygame.init()
pygame = pygame
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

fps = 60
pipe_interval = int(1000 * 60 / fps)



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def game(generation, high_score):
    birds = ga.get_population()

    # for bird in birds:
    #     print(bird.neural_network)
    # input()
    pipe_level = 1
    pipes = []
    done = False
    pygame.time.set_timer(USEREVENT + 1, pipe_interval)
    BackGround = Background('large.jpg', [0, 0])
    while not done:
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                exit()
            if event.type == USEREVENT + 1:
                pipes.append(Pipe(pipe_level))
                pipe_level += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bird in birds:
                    bird.up()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.up()
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    exit()

        for pipe in pipes:
            pipe.update()
            pipes = [pipe for pipe in pipes if not pipe.offscreen()]
            for bird in birds:
                if pipe.hit(bird):
                    # print("Score of this bird was", bird.score)
                    birds.remove(bird)
                    pass

        # Drawing pipes
        for pipe in pipes:
            pipe.show()

        pipes_to_right_of_bird = [pipe for pipe in pipes if pipe.distance_from_bird_to_end_of_gap > 0]
        closest_pipe_to_right_of_bird = 0
        if len(pipes_to_right_of_bird) > 0:
            closest_pipe_to_right_of_bird = min(pipes_to_right_of_bird,
                                                key=lambda pipe_lambda: pipe_lambda.distance_from_bird_to_end_of_gap)

        # draw target point
        target_point = [100 + closest_pipe_to_right_of_bird.distance_from_bird_to_end_of_gap if isinstance(
            closest_pipe_to_right_of_bird, Pipe) else width,
                        closest_pipe_to_right_of_bird.top + int(
                            closest_pipe_to_right_of_bird.gap / 2) if closest_pipe_to_right_of_bird else int(
                            height / 2)]

        pygame.draw.circle(screen, blue, target_point, 5)
        pygame.draw.line(screen, blue, [0, target_point[1]], [width, target_point[1]])
        pygame.draw.line(screen, blue, [target_point[0], 0], [target_point[0], height])

        curr_score = ga.get_best_unit().score
        if curr_score > high_score:
            high_score = curr_score

        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "Generation:{}".format(generation), True, blue),
            (10, 570))

        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "High Score:{}".format(high_score), True, blue),
            (150, 570))

        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "alive:{}".format(len(birds)), True, blue),
            (300, 570))

        for bird in birds:
            if bird.hit_walls():
                birds.remove(bird)
                continue
            bird.update()
            bird.horizontal_distance = target_point[0] - bird.x
            bird.height_difference = target_point[1] - bird.y
            bird.target_point = target_point
            if(generation<3):
                sim=True
            else:
                sim=False

            if bird.neural_network_make_decision(bird.horizontal_distance, bird.height_difference, bird.velocity,simulated=sim):
                bird.up()
            else:
                pass

        # Draw birds
        for bird in birds:
            bird.show()

        if not len(birds):
            pass
            done = True

        pygame.display.flip()
        clock.tick(fps)


ga = Genetic_Algorithm(population_size=50)

generation = 0
high_score = 0
while 1:
    generation += 1
    print("New game, Generation:", generation)
    game(generation, high_score)
    score = ga.get_best_unit().score
    print("Best bird", score, "\n")
    if score>high_score: high_score = score
    ga.next_generation()
# game()

# new_ga = Population(population_size=6)
# i = 0
# while 1:
#     i += 1
#     print("New game", i)
#     game()
#     new_ga.create_new_generation()

pygame.quit()
exit()
