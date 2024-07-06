# CSE423
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

def draw(x:int,y:int,r=1.0,g=1.0,b=1.0)->int:
    glPointSize(2)
    glColor3f(r,g,b)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glutPostRedisplay()


def findZone(dy,dx):
    if (abs(dx)>abs(dy)):
        if (dx>=0 and dy>=0):
            return 0
        elif (dx<0 and dy>=0):
            return 3
        elif (dx<0 and dy<0):
            return 4
        else:
            return 7
    else:
        if (dx>=0 and dy>=0):
            return 1
        elif (dx<0 and dy>=0):
            return 2
        elif (dx<0 and dy<0):
            return 5
        else:
            return 6
        
def eightwayfor(zone,x0,y0,x1,y1):
    if zone==1:
        x0,y0,x1,y1 = y0,x0,y1,x1
    elif zone==2:
        x0,y0,x1,y1 = y0, -x0, y1, -x1
    elif zone==3:
        x0,y0,x1,y1 = -x0, y0, -x1, y1
    elif zone==4:
        x0,y0,x1,y1 = -x0, -y0, -x1, -y1
    elif zone==5:
        x0,y0,x1,y1 = -y0, -x0, -y1, -x1
    elif zone==6:
        x0,y0,x1,y1 = -y0, x0, -y1, x1
    elif zone==7:
        x0,y0,x1,y1 = x0,-y0,x1,-y1
    return x0,y0,x1,y1    


def eightwayback(zone,x0,y0):
    if zone==1:
        x0,y0 = y0, x0
    elif zone==2:
        x0,y0 = -y0, x0
    elif zone==3:
        x0,y0 = -x0, y0
    elif zone==4:
        x0,y0= -x0, -y0
    elif zone==5:
        x0,y0= -y0, -x0
    elif zone==6:
        x0,y0 = y0, -x0
    elif zone==7:
        x0,y0 = x0,-y0
    return x0,y0


def drawLine(x0:int,y0:int,x1:int,y1:int,r=1.0,g=1.0,b=1.0):
    dy = y1 - y0
    dx = x1 - x0
    zone = findZone(dy,dx)
    # print(dy,dx,zone)
    if zone!=0:
        x0,y0,x1,y1 = eightwayfor(zone,x0,y0,x1,y1)
        dy = y1 - y0
        dx = x1 - x0
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy-dx)

    x,y = x0, y0
    # draw(x,y,r,g,b)
    while (x<x1):
        if d<=0:
            x+=1
            d+=dE
        else:
            x+=1
            y+=1
            d+=dNE
        if zone==0:
            nx,ny = x,y
        else:
            nx,ny = eightwayback(zone, x, y)
        
        draw(nx,ny,r,g,b)
    # print(f"Done with {x0,y0} -> {x1,y1}")


def header():
    global W_Height, W_Width
    #left arrow
    drawLine(50,W_Height-50,100,W_Height-50,0,0.75,1.00)
    drawLine(50,W_Height-50,75,W_Height-75,0,0.75,1.00)
    drawLine(50,W_Height-50,75,W_Height-25,0,0.75,1.00)
    #right cross
 
    drawLine(700,W_Height-75,750,W_Height-25,1.0,0.25,0.0)
    drawLine(750,W_Height-75,700,W_Height-25,1.0,0.25,0.0)
    #middle pause
    
    if not pause:
        drawLine(390,W_Height-25,390,W_Height-75,0.87,0.87,0.52)
        drawLine(410,W_Height-25,410,W_Height-75,0.87,0.87,0.52)
    else:
        drawLine(370,W_Height-25,370,W_Height-75,0.87,0.87,0.52)
        drawLine(370,W_Height-25,430,W_Height-50,0.87,0.87,0.52)
        drawLine(430,W_Height-50,370,W_Height-75,0.87,0.87,0.52)


def diamond():
    global diamondpos
    if diamondpos:
        x,y,r,g,b = diamondpos
        drawLine(x-25,y-25,x,y,r,g,b)
        drawLine(x-25,y-25,x,y-50,r,g,b)
        drawLine(x+25,y-25,x,y-50,r,g,b)
        drawLine(x+25,y-25,x,y,r,g,b)


def catcher():
    global catcherpos
    xp = catcherpos
    drawLine(xp,50,xp+50,20,1.0,1.0,1.0)
    drawLine(xp+50,20,xp+150,20,1.0,1.0,1.0)
    drawLine(xp+150,20,xp+200,50,1.0,1.0,1.0)
    drawLine(xp+200,50,xp,50,1.0,1.0,1.0)

        
def catchermove(movement):
    global catcherpos
    if movement>0 and catcherpos<600:
        catcherpos += 5+point/15
    elif movement<0 and catcherpos>0:
        catcherpos -= 5+point/15


def diamondfall():
    global diamondpos,gameon,point,speed
    if diamondpos:
        if catcherpos<=diamondpos[0]<=catcherpos+201 and (diamondpos[1]-50)<=50:
            point+=1
            print(f"Score: {point}")
            diamondpos = []
            speed = 1+(point)/10
        elif diamondpos[1]<=20:
            diamondpos = []
            gameon = False
            print(f"Game Over! Score: {point}")
            point = 0
        else:
            diamondpos[1] -= speed
            diamond()
    else:
        r,g,b = random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10
        x = random.randint(50,750)
        y = 900
        diamondpos.extend([x,y,r,g,b])


def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)
    
  
def display():
    global W_Height, W_Width
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)
    header()
    diamond()
    catcher()
    # drawPoints()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutPostRedisplay()
    glutSwapBuffers()


def animate():
    if gameon and not pause:
        diamondfall()
        catcher()
    glutPostRedisplay()
    # time.sleep(10)




def specialKeyListener(key, x, y):
    if key==GLUT_KEY_RIGHT:
        if not pause and gameon:
            catchermove(1)
    if key== GLUT_KEY_LEFT:
        if not pause and gameon:
            catchermove(-1)
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global gameon,pause
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            if (50<=x<=100) and (925<=W_Height-y<=975):
                if not gameon:
                    print("Starting Over")
                    gameon = True
            elif (370<=x<=430) and (925<=W_Height-y<=975):
                pause = not pause
                # print("Middle Pause")
            elif (700<=x<=750) and (925<=W_Height-y<=975):
                if gameon:
                    print(f"Goodbye! Score: {point}")
                else:
                    print(f"Goodbye!")
                # sys.exit("Ended")
                glutLeaveMainLoop()
                

    glutPostRedisplay()


gameon = True
point = 0
diamondpos = []
pause = False
speed = 1    
catcherpos = 300
W_Width = 800
W_Height = 1000
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"22101221_Catch The Diamonds")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

# glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)


glutMainLoop()
