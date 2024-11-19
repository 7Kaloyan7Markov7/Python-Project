import pygame

pygame.init()

#constants
screen_width = 1280
screen_height = 720
white = (255,255,255)
player_width_offset = 95
player_height_offset = 95

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
floor = pygame.image.load('test_floor.png').convert_alpha()
    
#customizes images
class Sprite:
    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0) , (frame * 64 + 16, 21, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

#player atributes
current_direction = 'down'
current_frame = 0
player_x = 0
player_y = 0
is_dashing = False
walking_speed = 10
dash_speed = 50

#stores player animations in list
def get_all_frames(file_path, width, height, scale):
    whole_image = pygame.image.load(file_path).convert_alpha()
    taking_frames = Sprite(whole_image)
    frames = []

    for i in range(0,5):
        frames.append(taking_frames.get_image(i, width, height, scale, white))
    
    return frames
    
#storing player animation lists in a dict with corespondive directions
animations = {}
animations['down'] = get_all_frames('down_animation.png', 31, 31, 3)
animations['up'] = get_all_frames('up_animation.png', 31, 31, 3)
animations['left'] = get_all_frames('left_animation.png', 31, 31, 3)
animations['right'] = get_all_frames('right_animation.png', 31, 31, 3)

#sword animations stored in lists
sword_animations= {'down':get_all_frames('white.png',48,39, 4),
                    'up':get_all_frames('white.png',48, 39, 4)}
sword_animations['right'] = get_all_frames('sword_right.png', 48,39,4)
sword_animations['left'] = get_all_frames('sword_left1.png', 48,39, 4)

#sword atributes
sword_not_picked_up = get_all_frames('sword_right.png', 48, 39, 4)[0] #idle floating animation
sword_x = 400
sword_y = 100
sword_float_speed = 0.5
sword_current_frame = 0
is_picked_up = False
is_hit_limit = False 
is_attacking = False
is_attack_done = True

#main game loop
run = True
while run:
    clock.tick(40)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()

    #sword idle animation
    if not is_picked_up:
        sword_y += sword_float_speed
        if sword_y >= 124 or sword_y <= 100:
            sword_float_speed *= -1 

    #creating hitboxes
    player_hit_box = animations['down'][0].get_rect(topleft = (player_x,player_y))
    sword_pick_up_box = sword_not_picked_up.get_rect(width  = 80, height = 80, centerx = sword_x + 120, centery = sword_y + 55)

    #walking
    is_walking = False
    if keys[pygame.K_a] and player_x > 0:
        player_x -= walking_speed
        current_direction = 'left'
        is_walking = True
    if keys[pygame.K_d] and player_x < screen_width - player_width_offset:
        player_x += walking_speed
        current_direction = 'right'
        is_walking = True
    if keys[pygame.K_w] and player_y > 0:
        player_y -= walking_speed
        current_direction = 'up'
        is_walking = True
    if keys[pygame.K_s] and player_y < screen_height - player_height_offset:
        player_y += walking_speed
        current_direction = 'down'
        is_walking = True
    #resets to first frame
    if not is_walking:
        current_frame = 0
    #changes frames
    if is_walking: current_frame = (current_frame + 1) % 5

    #dashing
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            is_dashing = False

    if keys[pygame.K_SPACE] and not is_dashing:
        is_dashing = True
        if current_direction == 'down':
            if dash_speed > screen_height - player_height_offset - player_y:
                player_y = screen_height - player_height_offset
            else:
                player_y += dash_speed
        elif current_direction == 'up':
            if dash_speed > player_y:
                player_y = 0
            else:
                player_y -= dash_speed
        elif current_direction == 'right':
            if dash_speed > screen_width - player_width_offset - player_x:
                player_x = screen_width - player_width_offset
            else:
                player_x += dash_speed
        elif current_direction == 'left':
            if dash_speed > player_x :
                player_x = 0
            else:
                player_x -= dash_speed

    #regulating position of the sword after being picked up
    if is_picked_up:
        if current_direction == 'left':
                sword_x = player_x - 87
                sword_y = player_y - 20
        elif current_direction == 'right':
                sword_x = player_x - 20
                sword_y = player_y - 20    

    #attack
    if is_picked_up:
        if pygame.mouse.get_pressed()[0] and not is_attacking and is_attack_done:
            is_attacking = True
            is_attack_done = False

    if is_attacking:
        sword_current_frame += 1
        if sword_current_frame >= 5:  # Assuming 5 frames for the attack animation
            sword_current_frame = 0
            is_attacking = False  # Attack is done
            is_attack_done = False  # Prevent immediate re-attack until the button is released
    
    if event.type == pygame.MOUSEBUTTONUP:
        is_attack_done = True

    #drawing 
    screen.blit(floor, (0,0))
    screen.blit(animations[current_direction][current_frame], (player_x, player_y))
    if not is_picked_up:
        screen.blit(sword_not_picked_up, (sword_x,sword_y))
    else:
        if current_direction != 'up' and current_direction != 'down':
            screen.blit(sword_animations[current_direction][sword_current_frame], (sword_x, sword_y))

    #checks if the sword is picked up
    if pygame.Rect.colliderect(player_hit_box, sword_pick_up_box): is_picked_up = True
    pygame.display.update()        

pygame.quit()