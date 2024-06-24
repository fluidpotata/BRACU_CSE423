from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(0,0)
    glEnd()


def draw_home():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    glVertex2f(-200,0)
    glVertex2f(200,0)

    glVertex2f(-200,0)
    glVertex2f(0,200)

    glVertex2f(0,200)
    glVertex2f(200,0)

    glVertex2f(-200,0)
    glVertex2f(-200,-200)

    glVertex2f(-200,-200)
    glVertex2f(200,-200)

    glVertex2f(200,-200)
    glVertex2f(200,0)

    glVertex2f(-50,-200)
    glVertex2f(-50,-100)

    glVertex2f(-50,-100)
    glVertex2f(50,-100)

    glVertex2f(50,-100)
    glVertex2f(50,-200)

    glEnd()


def drawShapes():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0,0.0,0.0)
    glVertex2f(0,200)
    glColor3f(0.0,1.0,0.0)
    glVertex2f(-200,0)
    glColor3f(0.0,0.0,1.0)
    glVertex2f(200,0)
    glEnd()



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-500.0,500,-500.0,500,0.0,1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) 
    # draw_points(250, 250)
    draw_home()
    drawShapes()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1024, 720)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Sapphire Alcove")
glutDisplayFunc(showScreen)

glutMainLoop()
