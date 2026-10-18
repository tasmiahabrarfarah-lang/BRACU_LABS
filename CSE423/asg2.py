from OpenGL.GL import *    
from OpenGL.GLUT import *  
from OpenGL.GLU import *    
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
ball_speed = 0.1
ball_size = 9
balls = []
freeze = False
blink = False
blink_counter = 0

# ===== Coordinate Conversion =====
def convert_coordinate(x, y):

    a = x - WINDOW_WIDTH//2
    b = WINDOW_HEIGHT//2 - y

    return float(a), float(b)

# ===== Draw Functions =====
def draw_point(x, y, size):
    """Draws a single point at (x, y) with given size."""
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    global ball_size, freeze
    if key == b' ':
        freeze = not freeze

        if freeze:
            print("Frozen")

        else:
            print("Unfrozen")

        glutPostRedisplay()
        return

def special_key_listener(key, x, y):
    global ball_speed, freeze
    if freeze:
        return
    if key == GLUT_KEY_UP:
        ball_speed *= 2
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        ball_speed = ball_speed/2
        print("Speed decreased")
    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global balls, blink, freeze

    if freeze:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
        if blink:
            print("Blink ON")
        else:
            print("Blink OFF")
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x, y = convert_coordinate(x, y)

        dx = random.choice([-1,1])
        dy = random.choice([-1,1])

        r = random.random()
        g = random.random()
        b = random.random()

        balls.append([x,y,dx,dy,r,g,b])

# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_WIDTH/2,
        WINDOW_WIDTH/2,
        -WINDOW_HEIGHT/2,
        WINDOW_HEIGHT/2,
        -1, 1)
    glMatrixMode(GL_MODELVIEW)

# ===== Display & Animation =====
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for ball in balls:

        if blink and (blink_counter // 1000) % 2 == 0:
            glColor3f(0, 0, 0)
        else:
            glColor3f(ball[4], ball[5], ball[6])

        draw_point(ball[0], ball[1], ball_size)

    glutSwapBuffers()

def animate():
    global blink_counter, blink_visible, balls, freeze

    if freeze:
        return

    for ball in balls:

        ball[0] += ball_speed * ball[2]
        ball[1] += ball_speed * ball[3]


        if ball[0] >= WINDOW_WIDTH/2 - ball_size:
            ball[2] *= -1

        if ball[0] <= -WINDOW_WIDTH/2 + ball_size:
            ball[2] *= -1

        if ball[1] >= WINDOW_HEIGHT/2 - ball_size:
            ball[3] *= -1

        if ball[1] <= -WINDOW_HEIGHT/2 + ball_size:
            ball[3] *= -1

    if blink:
        blink_counter += 1
    else:
        blink_counter = 0

    glutPostRedisplay()

# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"OpenGL Interactive Animation")
    setup_projection()

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()

# ===== Entry Point =====
if __name__ == "__main__":
    main()
