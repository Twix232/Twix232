import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 1400
screen_height = 480 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
clicked = False
game_over = 0
start_game = False

# define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# define colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# load images

# background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
# panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
# button images
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
start_img = pygame.image.load('img/buttons/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/buttons/exit_btn.png').convert_alpha()
# load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
# sword image
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


# create function for drawing text
def draw_text(text, font, text_col, x, y):
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
        # load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 140
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()

    def idle(self):
        # set variables to Idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint((-.2 * self.strength), (.2 * self.strength))
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), white)
        damage_text_group.add(damage_text)

        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to Hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to Idle animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset (self):
        self.alive = True
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 350, 'Knight', 30, 0, 10, 10, 10, 0)
goblin1 = Fighter(750, 354, 'Goblin', 15, 0, 5, 5, 5, 0)
goblin2 = Fighter(950, 354, 'Goblin', 15, 0, 5, 5, 5, 0)

goblin_list = []
goblin_list.append(goblin1)
goblin_list.append(goblin2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
goblin1_health_bar = HealthBar(760, screen_height - bottom_panel + 40, goblin1.hp, goblin1.max_hp)
goblin2_health_bar = HealthBar(760, screen_height - bottom_panel + 100, goblin2.hp, goblin2.max_hp)

#create buttons
restart_button = button.Button(screen, 635, 120, restart_img, 120, 30)
start_button =  button.Button(screen, 700, 150, start_img, 200, 30)
exit_button =  button.Button(screen, 900, 150, exit_img, 600, 30)


run = True
while run:

    clock.tick(fps)

    if start_game == False:
        # main menu
        screen.fill(red)
        # add buttons
        start_button.draw(screen)
        exit_button.draw(screen)
    else:
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

        # draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        # control player actions
        # reset action variables
        attack = False
        target = None
        # making sure mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, goblin in enumerate(goblin_list):
            if goblin.rect.collidepoint(pos):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if clicked == True:
                    attack = True
                    target = goblin_list[count]



        if game_over ==0:
            # player action
            if knight.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # look for player action
                        # attack
                        if attack == True and target != None:
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
            else:
                game_over = -1


            # enemy action
            for count, goblin in enumerate(goblin_list):
                if current_fighter == 2 + count:
                    if goblin.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # attack
                            goblin.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                    else:
                        current_fighter += 1

            # if all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1



        #check if all goblins are dead
        alive_goblins = 0
        for goblin in goblin_list:
            if goblin.alive == True:
                alive_goblins += 1
        if alive_goblins == 0:
            game_over = 1

        # check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (550, 50))
            if game_over == -1:
                screen.blit(defeat_img, (590, 50))
            if restart_button.draw():
                knight.reset()
                for goblin in goblin_list:
                    goblin.reset()
                    current_fighter = 1
                    action_cooldown
                    game_over = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

    pygame.display.update()

pygame.quit()
