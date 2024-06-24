from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


W_Width, W_Height = 1024,720
rainSpeed = 0.5
rainAngle = 0.0
bgColors = [0.0, 0.0, 0.0]


def init():
    global bgColors
    x,y,z = bgColors
    glClearColor(x,y,z,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70,	1,	1,	1000.0)


def specialKeyListener(key, x, y):
    global speed,rainAngle,bgColors
    # if key=='w':
    #     print(1)
    if key==GLUT_KEY_RIGHT:
        rainAngle += 0.1
        # print("Speed Increased")
    if key== GLUT_KEY_LEFT:		
        rainAngle -= 0.1
        # print("Speed Decreased")
    elif key == GLUT_KEY_UP:  
        bgColors = [min(i + 0.1, 1.0) for i in bgColors]
    elif key == GLUT_KEY_DOWN:  
        bgColors = [max(i - 0.1, 0.0) for i in bgColors]
    glutPostRedisplay()


class RainDrop:
    def __init__(self):
        self.x = random.randint(-180,180)
        self.y = random.randint(-180,180)
        self.speedx = 0.0 + rainAngle
        self.speedy = rainSpeed

rainDrop = [RainDrop() for i in range(100)]
        
def drawHome():
    global bgColors
    glLineWidth(3)
    glBegin(GL_LINES)
    avgSkyBrightness = sum(bgColors) / 3
    if avgSkyBrightness==1.0:
        avgSkyBrightness = 0.9
    houseColor = [max(0.5, 1.0 - avgSkyBrightness+0.1), 
                  max(0.5, 1.0 - avgSkyBrightness+0.1), 
                  max(0.5, 1.0 - avgSkyBrightness+0.1)] 

    glColor3f(*houseColor)

    glVertex2f(-100,0)
    glVertex2f(100,0)

    glVertex2f(-100,0)
    glVertex2f(0,100)

    glVertex2f(0,100)
    glVertex2f(100,0)

    glVertex2f(-100,0)
    glVertex2f(-100,-100)

    glVertex2f(-100,-100)
    glVertex2f(100,-100)

    glVertex2f(100,-100)
    glVertex2f(100,0)

    glVertex2f(-25,-100)
    glVertex2f(-25,-50)

    glVertex2f(-25,-50)
    glVertex2f(25,-50)

    glVertex2f(25,-50)
    glVertex2f(25,-100)

    glEnd()


def drawRaindrop(raindrop):
    global bgColors,rainAngle
    avgSkyBrightness = sum(bgColors) / 3  
    if avgSkyBrightness==1.0:
        avgSkyBrightness = 0.9
    rainBrightness = max(0.5, 1.0 - avgSkyBrightness+0.1)  
    glColor3f(rainBrightness, rainBrightness, rainBrightness)  
    glBegin(GL_LINES)
    glVertex2f(raindrop.x,raindrop.y)
    glVertex2f(raindrop.x+rainAngle, raindrop.y-5)
    glEnd()


def display():
    global bgColors
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(bgColors[0],bgColors[1], bgColors[2], 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    drawHome()

    # rainDrop = [RainDrop() for i in range(100)]
    for i in rainDrop:
        drawRaindrop(i)


    glutSwapBuffers()



def animate():
    #//codes for any changes in Models, Camera
    global rainAngle
    glutPostRedisplay()
    for j in rainDrop:
        j.x += rainAngle
        j.y -= j.speedy
        if j.y<-180:
            j.x = random.randint(-180,180)
            j.y = 180
        if j.x>180:
            j.x = -180
        elif j.x<-180:
            j.x = 180



glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 


wind = glutCreateWindow(b"22101221_Task_01")
init()

glutDisplayFunc(display)	
glutIdleFunc(animate)	
# glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)

glutMainLoop()