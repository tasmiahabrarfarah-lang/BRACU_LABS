from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random
import time


camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 1000
rand_var = 423


player_x = 0.0
player_y = 0.0
player_angle = 0.0


dir_x = 0.0
dir_y = 1.0

life = 5
score = 0
missed = 0
game_over = False


first_person = False
cheat_mode = False
cheat_vision = False


camera_height = 500.0
camera_radius = 707.0
camera_angle = 90.0


view_dx = 0.0
view_dy = 1.0


ENEMY_COUNT = 5
enemy_x = [0.0] * ENEMY_COUNT
enemy_y = [0.0] * ENEMY_COUNT
enemy_scale = [1.0] * ENEMY_COUNT
enemy_grow = [0.018, 0.022, 0.020, 0.024, 0.019]


BULLET_MAX = 50
bullets_x = [0.0] * BULLET_MAX
bullets_y = [0.0] * BULLET_MAX
bullets_dx = [0.0] * BULLET_MAX
bullets_dy = [0.0] * BULLET_MAX
bullet_active = [False] * BULLET_MAX
bullet_target = [-1] * BULLET_MAX
bullet_count = 0


cheat_fire_counter = 0.0

last_time = time.perf_counter()


def normalize_direction(x, y):
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return 0.0, 1.0
    return x / length, y / length


def rotate_direction(x, y, degrees):
    radians = math.radians(degrees)
    c = math.cos(radians)
    s = math.sin(radians)
    return x * c - y * s, x * s + y * c


def clamp_player():
    global player_x, player_y

    limit = GRID_LENGTH - 70
    player_x = max(-limit, min(limit, player_x))
    player_y = max(-limit, min(limit, player_y))


def respawn_enemy(index):

    while True:
        enemy_x[index] = random.uniform(-GRID_LENGTH + 70, GRID_LENGTH - 70)
        enemy_y[index] = random.uniform(-GRID_LENGTH + 70, GRID_LENGTH - 70)

        dx = enemy_x[index] - player_x
        dy = enemy_y[index] - player_y

        if dx * dx + dy * dy > 260 * 260:
            break

    enemy_scale[index] = random.uniform(0.80, 1.05)


    enemy_grow[index] = abs(enemy_grow[index])


def reset_game():
    global life, score, missed, game_over
    global player_x, player_y, player_angle, dir_x, dir_y
    global bullet_count, cheat_fire_counter
    global camera_height, camera_radius, camera_angle
    global first_person, cheat_mode, cheat_vision
    global view_dx, view_dy, last_time

    life = 5
    score = 0
    missed = 0
    game_over = False

    player_x = 0.0
    player_y = 0.0
    player_angle = 0.0
    dir_x = 0.0
    dir_y = 1.0

    first_person = False
    cheat_mode = False
    cheat_vision = False

    camera_height = 500.0
    camera_radius = 707.0
    camera_angle = 90.0

    view_dx = 0.0
    view_dy = 1.0

    bullet_count = 0
    cheat_fire_counter = 0.0
    last_time = time.perf_counter()

    i = 0
    while i < BULLET_MAX:
        bullet_active[i] = False
        bullet_target[i] = -1
        bullets_x[i] = 0.0
        bullets_y[i] = 0.0
        bullets_dx[i] = 0.0
        bullets_dy[i] = 0.0
        i += 1

    i = 0
    while i < ENEMY_COUNT:
        respawn_enemy(i)
        i += 1


def fire_bullet(target_index=-1):
    global bullet_count

    if game_over:
        return False

    i = 0
    while i < BULLET_MAX:
        if not bullet_active[i]:
            bullet_active[i] = True
            bullet_target[i] = target_index
            bullets_x[i] = player_x + dir_x * 155
            bullets_y[i] = player_y + dir_y * 155
            bullets_dx[i] = dir_x
            bullets_dy[i] = dir_y
            bullet_count += 1
            print("Player shoots!")
            return True
        i += 1

    return False


def enemy_in_line_of_sight(index):

    dx = enemy_x[index] - player_x
    dy = enemy_y[index] - player_y

    forward_distance = dx * dir_x + dy * dir_y


    if forward_distance <= 0:
        return False

    perpendicular_distance = abs(dx * dir_y - dy * dir_x)


    enemy_radius = 34 * enemy_scale[index]

    return perpendicular_distance <= enemy_radius


def nearest_enemy_in_line_of_sight():

    nearest = -1
    nearest_distance = 999999999.0

    i = 0
    while i < ENEMY_COUNT:
        if enemy_in_line_of_sight(i):
            dx = enemy_x[i] - player_x
            dy = enemy_y[i] - player_y
            distance_squared = dx * dx + dy * dy

            if distance_squared < nearest_distance:
                nearest_distance = distance_squared
                nearest = i
        i += 1

    return nearest


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():
    global player_x, player_y, player_angle

    glPushMatrix()
    glTranslatef(player_x, player_y, 0)
    glRotatef(player_angle, 0, 0, 1)

    if game_over:
        glTranslatef(0, 0, 110)
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 0, -110)

    glColor3f(0.25, 0.38, 0.10)
    glPushMatrix()
    glTranslatef(0, 0, 105)
    glScalef(0.95, 0.65, 1.45)
    glutSolidCube(80)
    glPopMatrix()

    # HEAD
    glColor3f(0.02, 0.02, 0.02)
    glPushMatrix()
    glTranslatef(0, 0, 218)
    gluSphere(gluNewQuadric(), 43, 12, 12)
    glPopMatrix()

    # LEFT LEG
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(-27, 0, 0)
    gluCylinder(gluNewQuadric(), 19, 13, 78, 10, 10)
    glPopMatrix()

    # RIGHT LEG
    glPushMatrix()
    glTranslatef(27, 0, 0)
    gluCylinder(gluNewQuadric(), 19, 13, 78, 10, 10)
    glPopMatrix()

    # LEFT ARM
    glColor3f(0.93, 0.82, 0.68)
    glPushMatrix()
    glTranslatef(-47, 0, 150)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 13, 78, 10, 10)
    glPopMatrix()

    # RIGHT ARM
    glPushMatrix()
    glTranslatef(47, 0, 150)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 13, 78, 10, 10)
    glPopMatrix()


    glColor3f(0.68, 0.68, 0.68)
    glPushMatrix()
    glTranslatef(0, 105, 152)
    glScalef(0.58, 2.25, 0.42)
    glutSolidCube(45)
    glPopMatrix()

    glPopMatrix()


    i = 0
    while i < ENEMY_COUNT:
        glPushMatrix()
        glTranslatef(enemy_x[i], enemy_y[i], 42)
        glScalef(enemy_scale[i], enemy_scale[i], enemy_scale[i])

        glColor3f(1, 0, 0)
        gluSphere(gluNewQuadric(), 34, 12, 12)

        glColor3f(0, 0, 0)
        glTranslatef(10, -7, 15)
        gluSphere(gluNewQuadric(), 18, 10, 10)

        glPopMatrix()
        i += 1


    glColor3f(1, 0.85, 0)
    i = 0
    while i < BULLET_MAX:
        if bullet_active[i]:
            glPushMatrix()
            glTranslatef(bullets_x[i], bullets_y[i], 42)
            glScalef(0.45, 0.45, 0.45)
            glutSolidCube(25)
            glPopMatrix()
        i += 1


def keyboardListener(key, x, y):
    global player_x, player_y, dir_x, dir_y, player_angle
    global cheat_mode, cheat_vision

    if key == b'r':
        if game_over:
            reset_game()
        return

    if key == b'c':
        if not game_over:
            cheat_mode = not cheat_mode
            return

    if key == b'v':
        if not game_over:
            cheat_vision = not cheat_vision
            return

    if game_over:
        return

    # Move forward
    if key == b'w':
        player_x += dir_x * 18
        player_y += dir_y * 18

    # Move backward
    if key == b's':
        player_x -= dir_x * 18
        player_y -= dir_y * 18

    # Rotate gun left
    if key == b'a':
        dir_x, dir_y = rotate_direction(dir_x, dir_y, 5)
        player_angle += 5
        if player_angle >= 360:
            player_angle -= 360

    # Rotate gun right
    if key == b'd':
        dir_x, dir_y = rotate_direction(dir_x, dir_y, -5)
        player_angle -= 5
        if player_angle < 0:
            player_angle += 360

    clamp_player()


def specialKeyListener(key, x, y):
    global camera_height, camera_angle, camera_pos
    global view_dx, view_dy

    if key == GLUT_KEY_UP:
        camera_height += 50
        if camera_height > 2200:
            camera_height = 2200

    if key == GLUT_KEY_DOWN:
        camera_height -= 50
        if camera_height < 150:
            camera_height = 150

    if key == GLUT_KEY_LEFT:
        if first_person:
            view_dx, view_dy = rotate_direction(view_dx, view_dy, 5)
        else:
            camera_angle += 5

    if key == GLUT_KEY_RIGHT:
        if first_person:
            view_dx, view_dy = rotate_direction(view_dx, view_dy, -5)
        else:
            camera_angle -= 5

    angle = math.radians(camera_angle)
    camera_pos = (
        camera_radius * math.cos(angle),
        camera_radius * math.sin(angle),
        camera_height
    )


def mouseListener(button, state, x, y):
    global first_person, view_dx, view_dy


    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_over:
            fire_bullet()


    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not game_over:
            first_person = not first_person
            if first_person:
                view_dx = dir_x
                view_dy = dir_y
            else:
                view_dx = dir_x
                view_dy = dir_y


def setupCamera():
    global camera_pos

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, GRID_LENGTH * 4.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:

        camx = player_x - dir_x * 75
        camy = player_y - dir_y * 75
        camz = 190

        if cheat_mode and cheat_vision:
            target_dx = dir_x
            target_dy = dir_y
        else:
            target_dx = view_dx
            target_dy = view_dy

        gluLookAt(
            camx, camy, camz,
            camx + target_dx * 400,
            camy + target_dy * 400,
            camz,
            0, 0, 1
        )
    else:
        angle = math.radians(camera_angle)
        camx = camera_radius * math.cos(angle)
        camy = camera_radius * math.sin(angle)
        camz = camera_height

        camera_pos = (camx, camy, camz)


        gluLookAt(
            camx, camy, camz,
            0, 0, 0,
            0, 0, 1
        )


def idle():
    global last_time, cheat_fire_counter
    global life, score, missed, game_over
    global player_x, player_y, dir_x, dir_y, player_angle
    global view_dx, view_dy, bullet_count

    current_time = time.perf_counter()
    dt = current_time - last_time
    last_time = current_time

 
    if dt > 0.05:
        dt = 0.05

    if not game_over:

        i = 0
        while i < ENEMY_COUNT:
            dx = player_x - enemy_x[i]
            dy = player_y - enemy_y[i]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                enemy_speed = 65.0 * dt
                enemy_x[i] += (dx / distance) * enemy_speed
                enemy_y[i] += (dy / distance) * enemy_speed

            enemy_scale[i] += enemy_grow[i] * (dt * 60.0)
            if enemy_scale[i] >= 1.25:
                enemy_scale[i] = 1.25
                enemy_grow[i] = -abs(enemy_grow[i])
            elif enemy_scale[i] <= 0.75:
                enemy_scale[i] = 0.75
                enemy_grow[i] = abs(enemy_grow[i])


            if distance < (48 + 34 * enemy_scale[i]):
                life -= 1
                print(f"Player life decreased! Life remaining: {life}")
                respawn_enemy(i)

                if life <= 0:
                    life = 0
                    game_over = True
                    break

            i += 1


        if cheat_mode and not game_over:

            rotation_speed = 120.0 * dt
            dir_x, dir_y = rotate_direction(dir_x, dir_y, -rotation_speed)
            player_angle -= rotation_speed
            if player_angle < 0:
                player_angle += 360

            if first_person and cheat_vision:
                view_dx = dir_x
                view_dy = dir_y

            cheat_fire_counter += dt
            if cheat_fire_counter >= 0.12:
                target = nearest_enemy_in_line_of_sight()
                if target != -1:

                    fire_bullet(target)
                cheat_fire_counter = 0.0

        bullet_speed = 900.0 * dt

        i = 0
        while i < BULLET_MAX:
            if bullet_active[i]:
                target_index = bullet_target[i]
                if cheat_mode and target_index >= 0 and target_index < ENEMY_COUNT:
                    tx = enemy_x[target_index] - bullets_x[i]
                    ty = enemy_y[target_index] - bullets_y[i]
                    target_distance = math.sqrt(tx * tx + ty * ty)
                    if target_distance > 0:
                        bullets_dx[i] = tx / target_distance
                        bullets_dy[i] = ty / target_distance

                bullets_x[i] += bullets_dx[i] * bullet_speed
                bullets_y[i] += bullets_dy[i] * bullet_speed

                hit = False
                j = 0
                while j < ENEMY_COUNT:
                    dx = bullets_x[i] - enemy_x[j]
                    dy = bullets_y[i] - enemy_y[j]
                    hit_radius = 42 * enemy_scale[j]

                    if dx * dx + dy * dy < hit_radius * hit_radius:
                        score += 1
                        respawn_enemy(j)
                        bullet_active[i] = False
                        bullet_target[i] = -1
                        bullet_count -= 1
                        hit = True
                        break
                    j += 1

                if not hit:
                    if (
                        bullets_x[i] > GRID_LENGTH + 40 or
                        bullets_x[i] < -GRID_LENGTH - 40 or
                        bullets_y[i] > GRID_LENGTH + 40 or
                        bullets_y[i] < -GRID_LENGTH - 40
                    ):
                        missed += 1
                        print(f"Bullet missed! Total missed: {missed}")
                        bullet_active[i] = False
                        bullet_target[i] = -1
                        bullet_count -= 1

                        if missed >= 10:
                            missed = 10
                            game_over = True
                            break
            i += 1

    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()


    GRID_TILES = 13
    tile_size = (GRID_LENGTH * 2) / GRID_TILES

    row = 0
    while row < GRID_TILES:
        col = 0
        while col < GRID_TILES:
            x1 = -GRID_LENGTH + col * tile_size
            y1 = -GRID_LENGTH + row * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size

            if (row + col) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            glBegin(GL_QUADS)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
            glEnd()

            col += 1
        row += 1


    wall_height = 70

    glBegin(GL_QUADS)

    # Left: blue
    glColor3f(0, 0, 1)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    # Right: green
    glColor3f(0, 1, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)

    # Far: cyan
    glColor3f(0, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    # Near: white
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glEnd()

    draw_text(35, 770, f"Player Life Remaining: {life}")
    draw_text(35, 740, f"Game Score: {score}")
    draw_text(35, 710, f"Player Bullet Missed: {missed}")

    if cheat_mode:
        draw_text(35, 680, "CHEAT MODE: ON")
        if cheat_vision and first_person:
            draw_text(35, 650, "AUTO GUN FOLLOW: ON")

    if first_person:
        draw_text(35, 620, "FIRST PERSON")

    if game_over:
        draw_text(400, 430, "GAME OVER")
        draw_text(350, 395, "Press R to Restart")

    draw_shapes()

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Assignment 3: Bullet Frenzy")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    random.seed(423)
    reset_game()
    main()