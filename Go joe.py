import pygame

pygame.init()

cube_width = 60
cube_height = 60
width = 1920
height = 1080
size = width, height

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Character Sprite
Joe_right = pygame.image.load('images/Joe_right.png')
Joe_left = pygame.image.load('images/Joe_left.png')
Joe_jump_right = pygame.image.load('images/Joe_jump_right.png')
Joe_jump_left = pygame.image.load('images/Joe_jump_left.png')
Joe = Joe_right  # initially facing right
Jolene = pygame.image.load('images/Jolene.png')

# Colours
white = (255, 255, 255)
beige = (235, 230, 210)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Physics Variables
x = 960
y = 800

velocity = pygame.Vector2(0, 0)
acceleration = 0.1
jump = 0

# Contacting Checks
on_surface = False
hit_wall = False
hit_top = False
charging = False
falling = False

# Ending Check
ending = False

font = pygame.font.Font('Bouncy_Font.otf', 100)
text = font.render('YOU WIN !', True, red, grey)
textRect = text.get_rect()
textRect.center = (960, 540)

# Repeating held inputs
pygame.key.set_repeat(20)

# Levels
level0 = {'blocks': [(0, 1080, 1920, 100)],
          'triangles': []}

level1 = {'blocks': [(600, 1030, 720, 50),  # long bottom
                     (0, 780, 600, 300),  # left big
                     (1320, 780, 600, 300),  # right big
                     (760, 440, 400, 100),  # middle
                     (1625, 225, 300, 100)],  # top right
          'triangles': [((1625, 225), (1625, 324), (1525, 324))]}

level2 = {'blocks': [(750, 930, 600, 100),  # long bottom
                     (0, 700, 500, 100),  # left tower base
                     (0, 450, 100, 100),  # first tower jump
                     (300, 200, 100, 100),  # second tower jump
                     (400, 200, 100, 350),  # right tower wall
                     (850, 350, 475, 100),  # top middle
                     (1525, 200, 250, 100)],  # top right
          'triangles': []}

level3 = {'blocks': [(1725, 925, 195, 100),  # right bottom
                     (1125, 925, 350, 100),  # left bottom
                     (951, 401, 199, 624),  # tower
                     (951, 0, 199, 150),  # top tower
                     (1475, 575, 200, 100),  # middle right
                     (500, 925, 200, 100),  # landing platform
                     (100, 675, 200, 100),  # first climb
                     (275, 325, 200, 100),  # second climb
                     (800, 100, 151, 50)],
          'triangles': [((1050, 300), (1050, 400), (950, 400)),
                        ((1050, 300), (1050, 400), (1150, 400))]}

level4 = {'blocks': [(951, 829, 199, 251),  # Tower
                     (200, 880, 400, 100),  # Left bottom
                     (1350, 0, 100, 575),  # bounce
                     (1150, 1010, 75, 75),  # landing platform
                     (300, 580, 300, 100),  # upper left bottom
                     (1700, 900, 150, 100),  # first climb
                     (1450, 475, 100, 100),  # second climb
                     (1775, 210, 75, 40)],  # third climb
          'triangles': [((951, 630), (951, 829), (1150, 829))]}

level5 = {'blocks': [(1350, 1030, 100, 50),  # small extension
                     (1050, 930, 400, 100),  # first long bottom
                     (500, 930, 400, 100),  # second long bottom
                     (1050, 350, 200, 450),  # right tower
                     (800, 400, 100, 400),  # left tower
                     (500, 400, 300, 100),  # left long top
                     (100, 650, 75, 75),  # free floating left
                     (1150, 250, 100, 100)],  # block after triangle
          'triangles': [((1149, 250), (1149, 350), (1050, 350))]}

level6 = {'blocks': [(0, 980, 850, 100),  # bottom left
                     (1270, 980, 650, 100),  # bottom right
                     (600, 680, 720, 61),  # tower base
                     (600, 0, 61, 500),  # left wall
                     (1259, 0, 61, 500),  # right wall
                     (825, 390, 270, 61),  # first tower jump
                     (875, 140, 170, 61)],  # second tower jump
          'triangles': []}

level7 = {'blocks': [(600, 700, 61, 61),  # top left wall
                     (600, 900, 61, 180),  # bottom left wall
                     (1259, 700, 61, 380),  # right wall
                     (925, 970, 70, 61),  # middle bottom platform
                     (705, 446, 510, 255),  # spire block
                     (400, 900, 200, 61),  # Balcony
                     (75, 675, 61, 61),  # first jump
                     (425, 450, 61, 61),  # second jump
                     (75, 100, 61, 61),  # third jump

                     (1200, 0, 61, 250),  # left tower wall Con.
                     (1375, 0, 61, 125),  # right tower wall Con.
                     (1200, 250, 236, 61),  # tower floor
                     (1634, 0, 61, 165),  # right tower left wall
                     (1634, 300, 286, 61),  # tower floor
                     (1859, 75, 61, 61)  # first tower stair
                     ],
          'triangles': [((960, 190), (960, 445), (705, 445)),  # top left
                        ((705, 445), (705, 700), (450, 700)),  # bottom left
                        ((960, 190), (960, 445), (1215, 445)),  # top right
                        ((1215, 445), (1215, 700), (1470, 700)),  # bottom right
                        ]}

level8 = {'blocks': [(450, 900, 200, 61),  # landing platform
                     (1200, 930, 61, 150),  # left tower wall
                     (1375, 930, 61, 150),  # right tower wall

                     (1634, 500, 61, 580),  # lower right tower left wall
                     (1634, 300, 61, 75),  # upper right tower left wall
                     (1634, 239, 286, 61),  # right tower roof
                     (1695, 980, 61, 61),  # second tower stair
                     (1859, 730, 61, 61),  # third tower stair
                     (1515, 500, 119, 61),  # balcony
                     (655, 375, 200, 61)  # middle jump
                     ],
          'triangles': [((1260, 869), (1260, 930), (1199, 930)),  # left tower spike
                        ((1375, 869), (1375, 930), (1436, 930))  # right tower spike
                        ]}

level9 = {'blocks': [(1634, 990, 130, 61),  # landing block
                     (1185, 675, 61, 176),  # first jump
                     (549, 775, 61, 176),  # second jump
                     (125, 475, 61, 126),  # third jump
                     (825, 200, 61, 126),  # fourth jump
                     (1325, 200, 61, 126),  # fifth jump
                     ],
          'triangles': [((1185, 675), (1185, 850), (1010, 850)),  # first jump
                        ((610, 775), (610, 950), (785, 950)),  # second jump
                        ((186, 475), (186, 600), (311, 600)),  # third jump
                        ((825, 200), (825, 325), (700, 325)),  # fourth jump
                        ((1386, 200), (1386, 325), (1511, 325)),  # fifth jump
                        ]}

level10 = {'blocks': [(1800, 900, 120, 61),  # bottom right
                      (1600, 0, 61, 125),  # top right wall
                      (1600, 300, 61, 250),  # bottom right wall
                      (1661, 300, 61, 61),  # right balcony
                      (259, 0, 61, 300),  # top left wall
                      (259, 400, 61, 150),  # bottom left wall
                      (320, 400, 61, 61),  # left balcony
                      (1250, 775, 61, 61),  # first jump
                      (450, 800, 61, 61),  # second jump
                      (175, 700, 61, 61),  # third jump
                      (1025, 300, 61, 61),  # fourth jump
                      (60, 199, 200, 20),  # slope bottom
                      ],
           'triangles': [((259, 1), (259, 199), (60, 199))  # killer
                         ]}

level11 = {'blocks': [(1600, 400, 61, 450),  # top right wall
                      (1600, 1000, 61, 80),  # bottom right wall
                      (1361, 1000, 361, 61),  # right balcony
                      (380, 950, 275, 61),  # left balcony
                      (490, 400, 1110, 61),  # top platform
                      (380, 1010, 60, 70),  # bottom by slope
                      (265, 575, 61, 61),  # last jump
                      (490, 461, 61, 264),  # bounce wall
                      (0, 425, 100, 61)  # no no no
                      ],
           'triangles': [((380, 950), (380, 1080), (250, 1080))
                         ]}

level12 = {'blocks': [],
           'triangles': []}

levels = {0: level0, 1: level1, 2: level2, 3: level3, 4: level4, 5: level5, 6: level6,
          7: level7, 8: level8, 9: level9, 10: level10, 11: level11, 12: level12}
current_level = 1

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        quit()
    for event in pygame.event.get():  # NEED THIS FOR LOOP
        if event.type == pygame.QUIT:
            quit()
        # # BugTesting #
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     x = event.__dict__['pos'][0]
        #     y = event.__dict__['pos'][1]
        #     velocity.y = -2
        #     velocity.x = 0
        #     if event.__dict__['button'] == 3:
        #         current_level += 1
        # Jump (only in air)
        if not falling:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and on_surface:
                    if Joe == Joe_right:
                        Joe = Joe_jump_right
                    if Joe == Joe_left:
                        Joe = Joe_jump_left
                    charging = True
                    jump += 1
                    velocity.x = 0
                if jump > 0:
                    if event.key == pygame.K_LEFT:
                        jump += 1
                        Joe = Joe_jump_left
                    if event.key == pygame.K_RIGHT:
                        jump += 1
                        Joe = Joe_jump_right
            if event.type == pygame.KEYUP and event.key == pygame.K_UP and on_surface:
                on_surface = False
                charging = False
                if Joe == Joe_jump_right:
                    Joe = Joe_right
                if Joe == Joe_jump_left:
                    Joe = Joe_left
                if jump > 40:
                    jump = 40
                velocity.y = - jump / 4
                if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                    velocity.x = 0
                elif keys[pygame.K_LEFT]:
                    velocity.x = - jump / 8
                elif keys[pygame.K_RIGHT]:
                    velocity.x = jump / 8
                jump = 0

    # General rules
    screen.fill(grey)
    screen.blit(Joe, (x, y))

    if current_level == 11:
        screen.blit(Jolene, (1500, 320))

    velocity.y += acceleration
    y += velocity.y
    x += velocity.x

    # Screen Borders
    if y > screen.get_height():
        y = 0
        current_level -= 1
    if y + cube_height < 0:
        y = screen.get_height()
        current_level += 1
    if x < 0:
        x = 0
        if not on_surface:
            hit_wall = True
    if x + cube_width > screen.get_width():
        x = screen.get_width() - cube_width
        if not on_surface:
            hit_wall = True

    # Horizontal Movement
    if on_surface and not charging:
        if keys[pygame.K_LEFT]:
            velocity.x = -3
        elif keys[pygame.K_RIGHT]:
            velocity.x = 3
        else:
            velocity.x = 0

    # Drawing Blocks and getting dimensions
    for i in levels[current_level]['blocks']:
        pygame.draw.rect(screen, black, i)
        left = i[0]
        right = i[0] + i[2]
        top = i[1]
        bottom = i[1] + i[3]

        # Block Contacts
        if bottom > y and y + cube_height > top and x + cube_width > left and x < right:

            # Top Right corners
            if x > left and y + cube_height < bottom:
                top_overlap = right - x
                side_overlap = y + cube_height - top
                if side_overlap > top_overlap:
                    x = right
                    if not on_surface:
                        hit_wall = True
                else:
                    y = top - cube_height
                    velocity.y = 0
                    falling = False
                    on_surface = True

            # Bottom Right corners
            elif y > top and x > left:
                bottom_overlap = right - x
                side_overlap = bottom - y
                if side_overlap > bottom_overlap:
                    x = right
                    if not on_surface:
                        hit_wall = True
                else:
                    y = bottom
                    hit_top = True

            # Top Left Corners
            elif x + cube_width < right and y + cube_height < bottom:
                top_overlap = x + cube_width - left
                side_overlap = y + cube_height - top
                if side_overlap > top_overlap:
                    x = left - cube_width
                    if not on_surface:
                        hit_wall = True
                else:
                    y = top - cube_height
                    velocity.y = 0
                    falling = False
                    on_surface = True

            # Bottom Left corners
            elif y > top and x + cube_width < right:
                bottom_overlap = x + cube_width - left
                side_overlap = bottom - y
                if side_overlap > bottom_overlap:
                    x = left - cube_width
                    if not on_surface:
                        hit_wall = True
                else:
                    y = bottom
                    hit_top = True

    # Drawing triangles

    for triangle in levels[current_level]['triangles']:
        pygame.draw.polygon(screen, black, triangle, 0)
        point1x = triangle[0][0]
        point1y = triangle[0][1]
        point2x = triangle[1][0]
        point2y = triangle[1][1]
        point3x = triangle[2][0]
        point3y = triangle[2][1]

        bottom = point2y
        side = point1x
        non_side = point3x
        top = point1y
        if point3x < point2x:  # Left triangle
            left_triangle = True
            right_triangle = False
        else:  # Right triangle
            left_triangle = False
            right_triangle = True

        if left_triangle:
            if bottom > y and y + cube_height > top and x + cube_width > non_side and x < side:

                # Bottom right corners
                if y > top and x > non_side:
                    if x + cube_width > side or y >= bottom:
                        bottom_overlap = side - x
                        side_overlap = bottom - y
                        if side_overlap > bottom_overlap:
                            x = side
                            if not on_surface:
                                hit_wall = True
                        else:
                            y = bottom
                            hit_top = True

                # Top Right Corners
                if x > non_side and y + cube_height < bottom:
                    if x + cube_width > side and y < top:
                        top_overlap = side - x
                        side_overlap = y + cube_height - top
                        if side_overlap < top_overlap:
                            if x + cube_width / 2 > side:
                                y = top - cube_height
                                velocity.y = 0
                                falling = False
                                on_surface = True
                            else:
                                x = side - cube_width
                                falling = True
                        else:
                            x = side
                            if not on_surface:
                                hit_wall = True

                # Bottom left corners
                if y > top and x + cube_width < side:
                    if x < non_side or y + cube_height > bottom:
                        bottom_overlap = x + cube_width - non_side
                        side_overlap = bottom - y
                        if side_overlap > bottom_overlap:
                            if y + cube_height >= bottom:
                                x = non_side - cube_width
                                if not on_surface:
                                    hit_wall = True
                        else:
                            y = bottom
                            hit_top = True

                # Slope
                if x + cube_width <= side and y + cube_height < bottom:
                    if x + cube_width > non_side or y < top:
                        if x + cube_width <= side and x + cube_width > non_side:
                            y_int = point1x + point1y
                            if (y + cube_height > -(x + cube_width) + y_int) and (y + cube_height < bottom):
                                y = -(x + cube_width) + y_int - cube_height
                                velocity.x = - velocity.y

        elif right_triangle:
            if bottom > y and y + cube_height > top and x + cube_width > side and x < non_side:

                # Bottom Left corners
                if y > top and x + cube_width < non_side:
                    if x < side or y + cube_height > bottom:
                        bottom_overlap = x + cube_width - side
                        side_overlap = bottom - y
                        if side_overlap > bottom_overlap:
                            x = side - cube_width
                            if not on_surface:
                                hit_wall = True
                        else:
                            y = bottom
                            hit_top = True

                # Top Left Corners
                elif x + cube_width < non_side and y + cube_height < bottom:
                    if x < side and y < top:
                        top_overlap = x + cube_width - side
                        side_overlap = y + cube_height - top
                        if side_overlap < top_overlap:
                            if x + cube_width / 2 < side:
                                y = top - cube_height
                                velocity.y = 0
                                falling = False
                                on_surface = True
                            else:
                                x = side
                                falling = True
                        else:
                            x = side - cube_width
                            if not on_surface:
                                hit_wall = True

                # Bottom Right corners
                elif y > top and x > side:
                    if x + cube_width > non_side or y + cube_height > bottom:
                        bottom_overlap = non_side - x
                        side_overlap = bottom - y
                        if side_overlap > bottom_overlap or y + cube_height > bottom:
                            if y + cube_height >= bottom:
                                x = non_side
                                if not on_surface:
                                    hit_wall = True
                        else:
                            y = bottom
                            hit_top = True

                # Slope
                if x >= side and y + cube_height < bottom:
                    if x < non_side or y < top:
                        if x >= side and x < non_side:
                            y_int = point1y - point1x
                            if (y + cube_height > x + y_int) and (y + cube_height < bottom):
                                y = x + y_int - cube_height
                                velocity.x = velocity.y

    # Doing Contact Actions
    if hit_wall:
        velocity.x = - velocity.x / 2
        hit_wall = False

    if hit_top:
        velocity.y = - velocity.y / 2
        hit_top = False

    if velocity.y > 0.1:
        falling = True
        on_surface = False

    # Y Velocity Cap
    if velocity.y > 10:
        velocity.y = 10

    # Checking Position
    if velocity.x > 0:
        Joe = Joe_right
    if velocity.x < 0:
        Joe = Joe_left

    if x > 1400 and y < 425 and current_level == 11:
        ending = True

    if ending:
        screen.blit(text, textRect)

        if keys[pygame.K_ESCAPE]:
            quit()
        for event in pygame.event.get():  # NEED THIS FOR LOOP
            if event.type == pygame.QUIT:
                quit()

    pygame.display.update()
    pygame.time.delay(5)
