from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint


def drawPoint(x,y, r, g, b):
    glPointSize(5)
    glColor3f(r,g,b)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawPoints():
    global randomPoints,speed,blink,freeze
    for i in range(len(randomPoints)):
        if not freeze:
            randomPoints[i][0] += randomPoints[i][5][0]*speed
            randomPoints[i][1] += randomPoints[i][5][1]*speed
            if randomPoints[i][0]>1080 or randomPoints[i][0]<0 :
                randomPoints[i][5][0] *= -1
            if randomPoints[i][1]>720 or randomPoints[i][1]<0:
                randomPoints[i][5][1] *= -1
        if not blink: 
            drawPoint(randomPoints[i][0],randomPoints[i][1], randomPoints[i][2], randomPoints[i][3], randomPoints[i][4])
        else:
            drawPoint(randomPoints[i][0],randomPoints[i][1], 0.0, 0.0, 0.0)
        glutPostRedisplay()


def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global randomPoints,speed, blink
    if button==GLUT_RIGHT_BUTTON:
        if(state == GLUT_DOWN):
            # print(f"Found in {x,y}")
            y = glutGet(GLUT_WINDOW_HEIGHT) - y
            possible_moves = ([-1, 1], [-1, -1], [1,1],  [1, -1])
            r,g,b = randint(1,10)/10, randint(1,10)/10, randint(1,10)/10
            move = randint(0,3)
            randomPoints.append([x,y,r,g,b,possible_moves[move]])
            drawPoint(x,y,r,g,b)




    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            blink = not blink
    # case GLUT_MIDDLE_BUTTON:
    #     //........

    glutPostRedisplay()


def keyboardListener(key, x, y):
    global freeze
    if key==b' ':
        freeze = not freeze
    if key==b's':
        ball_size-=1
        print("Size Decreased")


def specialKeyListener(key, x, y):
    global speed
    if key==GLUT_KEY_UP:
        speed *= 2
        # print("Speed Increased")
    if key== GLUT_KEY_DOWN:		#// up arrow key
        speed /= 2
        # print("Speed Decreased")
    glutPostRedisplay()

def display():
    global W_Height, W_Width
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

    drawPoints()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutSwapBuffers()



def animate():
    drawPoints()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)


freeze = False
randomPoints = []
speed = 0.5
blink = False

W_Width = 1080
W_Height = 720
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"22101221_task02")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()