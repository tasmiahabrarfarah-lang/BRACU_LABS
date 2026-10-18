#task 1
from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1750, 750
rain_x, rain_y = 0, 750        # Ball coordinates (in OpenGL space)
rain_speed = 0.01            # Ball movement speed
rain_angle=0
skyshade=0

# ===== Draw Functions =====
def draw_rain(angle):
    """Draws a single point at (x, y) with given size."""
    glLineWidth(1)
    glBegin(GL_LINES)
    for i in range(20):
#blue rain
        glColor3f(0.0, 0.0, 1.0)
        x=random.randint(0,1750)
        y=random.randint(0,750)
        glVertex2f(x,y)
        glVertex2f(x+angle,y+40)

#white rain
        glColor3f(1, 1, 1)
        x=random.randint(0,1750)
        y=random.randint(0,750)
        glVertex2f(x,y)
        glVertex2f(x+angle,y+40)

    glEnd()

def draw_axes():
    """Draws X and Y axes centered at origin."""
    glLineWidth(2)
    glBegin(GL_LINES)
    # right
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(862.5, 362.5)
    glVertex2f(962.5, 362.5)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(912.5, 325)
    glVertex2f(912.5, 400)

    # left
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(562.5, 362.5)
    glVertex2f(662.5, 362.5)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(612.5, 325)
    glVertex2f(612.5, 400)
    glEnd()

#roof outline
    glLineWidth(1)
    glBegin(GL_LINES)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(337.5, 475)
    glVertex2f(1187.5, 475)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(337.5, 475)
    glVertex2f(762.5, 575)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(762.5, 575)
    glVertex2f(1187.5, 475)
    glEnd()

#house outline
    glLineWidth(1)
    glBegin(GL_LINES)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(387.5, 475)
    glVertex2f(1137.5, 475)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(387.5, 275)
    glVertex2f(1137.5, 275)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(387.5, 275)
    glVertex2f(387.5, 475)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(1137.5, 275)
    glVertex2f(1137.5, 475)
    
    glEnd()

#door outline
    glLineWidth(1)
    glBegin(GL_LINES)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(712.5, 275)
    glVertex2f(812.5, 275)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(712.5, 400)
    glVertex2f(812.5, 400)


    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(712.5, 275)
    glVertex2f(712.5, 400)

    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(812.5, 275)
    glVertex2f(812.5, 400)
    glEnd()

def sky(skyshade):
    glBegin(GL_TRIANGLES)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(1750,0)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(0,750)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(0,475)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(1750,0)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(0,750)
    glColor3f(0,0+skyshade,1+skyshade)
    glVertex2d(1750,750)
    glEnd()


def draw_shapes():
    """Draws a triangle and a square with color gradients."""

    # bg
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.2, 0.0)
    glVertex2d(1750,0)
    glColor3f(0.0,0.2,0.0)
    glVertex2d(1750,550)
    glColor3f(0.0,0.2,0.0)
    glVertex2d(0,550)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.2, 0.0)
    glVertex2d(1750,0)
    glColor3f(0.0, 0.2, 0.0)
    glVertex2d(0,0)
    glColor3f(0.0, 0.2, 0.0)
    glVertex2d(0,550)
    glEnd()

#grass
    j=0
    for i in range(0,1700,50):
        glBegin(GL_TRIANGLES)
        glColor3f(0,0.6+j,0.3-j/2)
        glVertex2d(i,400)
        glColor3f(0,0.6+j,0.3-j/2)
        glVertex2d(i+85,400)
        glColor3f(0.0, 0.2, 0.0)
        glVertex2d((2*i+85)/2,500)
        glEnd()
        j+=0.0267

    # house box
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.71, 0.75)
    glVertex2d(387.5,475)
    glColor3f(0.4,0.7,1)
    glVertex2d(1137.5,475)
    glColor3f(1.0, 0.71, 0.75)
    glVertex2d(1137.5,275)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.71, 0.75)
    glVertex2d(387.5,475)
    glColor3f(0.4,0.7,1)
    glVertex2d(387.5,275)
    glColor3f(1.0, 0.71, 0.75)
    glVertex2d(1137.5,275)
    glEnd()

#doorbox
    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.3, 1)
    glVertex2d(812.5,275)
    glColor3f(0.3,0.7,1)
    glVertex2d(812.5,400)
    glColor3f(1,0,1)
    glVertex2d(762.5,337.5)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.3, 1)
    glVertex2d(812.5,275)
    glColor3f(0.3,0.7,1)
    glVertex2d(712.5,275)
    glColor3f(1,0,1)
    glVertex2d(762.5,337.5)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.3, 1)
    glVertex2d(712.5,400)
    glColor3f(0.3,0.7,1)
    glVertex2d(712.5,275)
    glColor3f(1,0,1)
    glVertex2d(762.5,337.5)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.3, 1)
    glVertex2d(812.5,400)
    glColor3f(0.3,0.7,1)
    glVertex2d(762.5,337.5)
    glColor3f(1,0,1)
    glVertex2d(712.5,400)
    glEnd()

#right window
    glBegin(GL_TRIANGLES)
    glColor3f(1,1,1)
    glVertex2d(862.5,400)
    glColor3f(0.53, 0.81, 0.98)
    glVertex2d(962.5,400)
    glColor3f(1,1,1)
    glVertex2d(962.5,325)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1,1,1)
    glVertex2d(862.5,400)
    glColor3f(0.53, 0.81, 0.98)
    glVertex2d(862.5,325)
    glColor3f(1,1,1)
    glVertex2d(962.5,325)
    glEnd()

#left window
    glBegin(GL_TRIANGLES)
    glColor3f(0.53, 0.81, 0.98)
    glVertex2d(662.5,400)
    glColor3f(1,1,1)
    glVertex2d(562.5,400)
    glColor3f(1,1,1)
    glVertex2d(662.5,325)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.53, 0.81, 0.98)
    glVertex2d(562.5,325)
    glColor3f(1,1,1)
    glVertex2d(662.5,325)
    glColor3f(1,1,1)
    glVertex2d(562.5,400)
    glEnd()

#roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.68, 0.3, 1)
    glVertex2d(1187.5,475)
    glColor3f(0.5, 0.7, 1)
    glVertex2d(337.5,475)
    glColor3f(0.7, 0.6, 1)
    glVertex2d(762.5,575)
    glEnd()

#doorknob
    glBegin(GL_TRIANGLES)
    glColor3f(0,0,0)
    glVertex2d(797.5,332.5)
    glColor3f(0,0,0)
    glVertex2d(797.5,342.5)
    glColor3f(0,0,0)
    glVertex2d(787.5,342.5)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0,0,0)
    glVertex2d(797.5,332.5)
    glColor3f(0,0,0)
    glVertex2d(787.5,332.5)
    glColor3f(0,0,0)
    glVertex2d(787.5,342.5)
    glEnd()


# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global skyshade
    if key == b'w':  
        if skyshade<1:
            skyshade+=0.1
    elif key == b's':  
        if skyshade>0:
            skyshade-=0.1
    glutPostRedisplay()


def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    global rain_angle
    if key == GLUT_KEY_RIGHT:
        if rain_angle>-150:
            rain_angle=(rain_angle-20)
    elif key == GLUT_KEY_LEFT:
        if rain_angle<150:
            rain_angle=(rain_angle+20)
    glutPostRedisplay()

# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Display & Animation =====
def display():
    """Main display callback for rendering each frame."""
    global skyshade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    glColor3f(0+skyshade, 0+skyshade, 0+skyshade)   
    sky(skyshade)
    draw_shapes()
    draw_axes()
    draw_rain(rain_angle)
    glutSwapBuffers()
 

def animate():
    """Continuously moves the rain diagonally."""
    global rain_x, rain_y, rain_speed
    rain_x = (rain_x + rain_speed) % 180
    rain_y = (rain_y + rain_speed) % 180
    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"OpenGL Interactive Animation")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()







#task 2
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
