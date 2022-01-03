
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 1400
screen_height = 480 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#define game variables
current_fighter = 1


# define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# define colors
red = (255, 0, 0)
green = (0, 255, 0)

# load images
# background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
# panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()


# create function for drawing text
def draw_text(text, font, text_col, x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


# function for drawing panel
def draw_panel():
    # draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(goblin_list):
        # show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 760, (screen_height - bottom_panel + 10) + count * 60)



# fighter class
class Fighter():
    def __init__(self, x, y, name, max_health, max_mana, strength, defense, agility, intelligence):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.hp = max_health
        self.max_hp = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.mp = max_mana
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.intelligence = intelligence
        self.magic = intelligence
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new hp
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150, 20))




knight = Fighter(200, 350, 'Knight', 30, 30, 10, 3, 3, 3)
goblin1 = Fighter(750, 350, 'Goblin', 20, 0, 6, 1, 3, 3)
goblin2 = Fighter(900, 350, 'Goblin', 20, 0, 6, 1, 3, 3)

goblin_list = []
goblin_list.append(goblin1)
goblin_list.append(goblin2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
goblin1_health_bar = HealthBar(760, screen_height - bottom_panel + 40, goblin1.hp, goblin1.max_hp)
goblin2_health_bar = HealthBar(760, screen_height - bottom_panel + 100, goblin2.hp, goblin2.max_hp)


run = True
while run:

    clock.tick(fps)

    # draw background
    draw_bg()

    # draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    goblin1_health_bar.draw(goblin1.hp)
    goblin2_health_bar.draw(goblin2.hp)


    # draw fighters
    knight.update()
    knight.draw()
    for goblin in goblin_list:
        goblin.update()
        goblin.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
