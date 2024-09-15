from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


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
        
def eightwayfor(zone,x0,y0):
    if zone==1:
        x0,y0 = y0, x0
    elif zone==2:
        x0,y0 = y0, -x0
    elif zone==3:
        x0,y0 = -x0, y0
    elif zone==4:
        x0,y0 = -x0, -y0
    elif zone==5:
        x0,y0 = -y0, -x0
    elif zone==6:
        x0,y0 = -y0, x0
    elif zone==7:
        x0,y0 = x0,-y0
    return x0,y0

def eightwayback(zone,x0,y0):
    if zone==1:
        x0,y0 = y0, x0
    elif zone==2:
        x0,y0 = -y0, x0
    elif zone==3:
        x0,y0 = -x0, y0
    elif zone==4:
        x0,y0 = -x0, -y0
    elif zone==5:
        x0,y0 = -y0, -x0
    elif zone==6:
        x0,y0 = y0, -x0
    elif zone==7:
        x0,y0 = x0, -y0
    return x0,y0


def drawLine(x0:int,y0:int,x1:int,y1:int,r=1.0,g=1.0,b=1.0):
    dy = y1 - y0
    dx = x1 - x0
    zone = findZone(dy,dx)
    if zone!=0:
        x0,y0 = eightwayfor(zone,x0,y0)
        x1,y1 = eightwayfor(zone,x1,y1)
        dy = y1 - y0
        dx = x1 - x0
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy-dx)

    x,y = x0, y0
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


def header():
    global W_Height, W_Width
    #left arrow
    drawLine(50-W_Width/2,(W_Height/2)-50,100-W_Width/2,(W_Height/2)-50,0,0.75,1.00)
    drawLine(50-W_Width/2,(W_Height/2)-50,75-W_Width/2,(W_Height/2)-75,0,0.75,1.00)
    drawLine(50-W_Width/2,(W_Height/2)-50,75-W_Width/2,(W_Height/2)-25,0,0.75,1.00)
    #right cross
    drawLine(700-W_Width/2,(W_Height/2)-75,750-W_Width/2,(W_Height/2)-25,1.0,0.25,0.0)
    drawLine(750-W_Width/2,(W_Height/2)-75,700-W_Width/2,(W_Height/2)-25,1.0,0.25,0.0)
    #middle pause
    
    if not pause:
        drawLine(390-W_Width/2,(W_Height/2)-25,390-W_Width/2,(W_Height/2)-75,0.87,0.87,0.52)
        drawLine(410-W_Width/2,(W_Height/2)-25,410-W_Width/2,(W_Height/2)-75,0.87,0.87,0.52)
    else:
        drawLine(370-W_Width/2,(W_Height/2)-25,370-W_Width/2,(W_Height/2)-75,0.87,0.87,0.52)
        drawLine(370-W_Width/2,(W_Height/2)-25,430-W_Width/2,(W_Height/2)-50,0.87,0.87,0.52)
        drawLine(430-W_Width/2,(W_Height/2)-50,370-W_Width/2,(W_Height/2)-75,0.87,0.87,0.52)


def draw8way(x,y,h,k,r=1.0,g=1.0,b=1.0):
    draw(x+h,y+k)
    for i in range(1,9):
        xp,yp = eightwayfor(i,x,y)
        draw(xp+h,yp+k,r,g,b)


def drawCircle_zone0(r:int,h:int=0,k:int=0,red=1.0,g=1.0,b=1.0):
    d = 1-r
    x,y = r,0
    draw8way(x,y,h,k,red,g,b)
    while (x>=y):
        if d>0:
            d += 2*y - 2*x + 5
            x -= 1
            y += 1
        else:
            d += 2*y + 3
            y = y+1
        draw8way(x,y,h,k,red,g,b)


def drawShooter():
    global  shooterPos
    if gameon:
        drawCircle_zone0(25, shooterPos[0], shooterPos[1])
    else:
        drawCircle_zone0(25, shooterPos[0], shooterPos[1],1.0,0.0,0.0)
    glutPostRedisplay()


def shooterMove(p):
    global  shooterPos
    if (gameon and not pause):
        if (p<0 and -375< shooterPos[0]) or (p>0 and  shooterPos[0]<375):
             shooterPos[0] += p


def drawBalls():
    global ballpos
    for i in ballpos:
        if i[3]:
            drawCircle_zone0(i[0],i[1],i[2],i[4],i[5],i[6])
    glutPostRedisplay()


def fallingBalls():
    global ballpos, pause, gameon, ballspeed, point, life, lastball, balls, shooterPos
    if gameon and not pause:
        next = True
        for i in range(len(ballpos)):
            if ballpos[i][3]:
                ballpos[i][2] -= ballspeed
                if ballpos[i][2]>300:
                    next = False
                d = ((ballpos[i][1]- shooterPos[0])**2 + (ballpos[i][2]- shooterPos[1])**2)**(0.5)
                if d<=(ballpos[i][0]+25):
                     gameon = False
                     print(f"Game over! score: {point}")
                if ballpos[i][2] <= (-500 + ballpos[i][0]):
                    removeBall(i)
                    life -= 1
                    print("1 life deduced")
                    if life == 0:
                        gameon = False
                        print(f"Game Over! Score: {point}")

        if next and balls<5:
            lastball = (lastball+1)%5
            ballpos[lastball][2],ballpos[lastball][3] = 375, True
            balls += 1
            # print("Balls",balls) 
    glutPostRedisplay()


    
def removeBall(i):
    global ballpos, balls
    ballpos[i] = [random.randint(25,40),random.randint(-375,375),375, True, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10]
    # ballpos.pop(i)
    # ballpos[i].append([random.randint(25,40),random.randint(-375,375),650, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10])
    # balls = balls-1     

def shootingBalls():
    global shootingballs
    for i in shootingballs:
        drawCircle_zone0(15,i[0],i[1])
    glutPostRedisplay()

def shootingMove():
    global shootingballs, ballspeed, ballpos, point, bullspeed, balls, pause, bullets, gameon
    for i in range(len(shootingballs)):
        if shootingballs:
            try:
                shootingballs[i][1] += bullspeed
                if shootingballs[i][1]>=400:
                    shootingballs.pop(i)
                    bullets -= 1
                    if bullets==0:
                        gameon = False
                        print(f"Game Over! Score {point}")
                    break
                for j in range(len(ballpos)):
                    d = ((ballpos[j][1]-shootingballs[i][0])**2 + (ballpos[j][2]-shootingballs[i][1])**2)**(0.5)
                    # print(ballpos)
                    # print(d)
                    if d<=ballpos[j][0]+15:
                        # print("YES")
                        removeBall(j)
                        shootingballs.pop(i)
                        point += 1
                        print(point)
                        break
            except:
                pass

    glutPostRedisplay()


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
    # gluOrtho2D(0, W_Width, 0, W_Height)
    gluOrtho2D(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2)
    # drawPoints()
    header()
    # drawCircle_zone0(100,100,-100)
    drawShooter()
    if gameon:
        drawBalls()
        shootingBalls()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutPostRedisplay()
    glutSwapBuffers()


def animate():
    if gameon and not pause:
        drawShooter()
        # drawBalls()
        fallingBalls()
        shootingMove()
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global gameon,pause, shooterPos,shooterSpeed,ballspeed,ballpos,shootingballs,bullspeed,life,lastball,balls,bullets,point
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            if (50<=x<=100) and (925<=W_Height-y<=975):
                if not gameon:
                    print("Starting Over")
                    shooterPos = [0,-465]
                    shooterSpeed = 8
                    ballpos = [[random.randint(25,40),random.randint(-375,375),375, True, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10]]
                    shootingballs = []
                    bullspeed = 12
                    life = 3
                    lastball = 0
                    balls = 1
                    bullets = 3
                    point = 0
                    gameon = True
                    pause = False
            elif (370<=x<=430) and (925<=W_Height-y<=975):
                pause = not pause
                print("Middle Pause")
            elif (700<=x<=750) and (925<=W_Height-y<=975):
                if gameon:
                    print(f"Goodbye! Score: {point}")
                else:
                    print(f"Goodbye!")
                # sys.exit("Ended")
                glutLeaveMainLoop()
                

    glutPostRedisplay()


def keyboardListener(key, x, y):
    global shooterSpeed,  shooterPos, shootingballs, gameon, pause
    if gameon and not pause:
        if key==b'a':
            shooterMove(-shooterSpeed)


        if key==b'd':
            shooterMove(shooterSpeed)


        if key==b' ':
            shootingballs.append([ shooterPos[0], -465])



shooterPos = [0,-465]
shooterSpeed = 8
ballspeed = 1
ballpos = [[random.randint(25,40),random.randint(-375,375),375, True, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10],
           [random.randint(25,40),random.randint(-375,375),600, False, random.randint(6,11)/10,random.randint(6,11)/10,random.randint(6,11)/10]]
shootingballs = []
bullspeed = 12
life,bullets = 3,3
lastball = 0
balls = 1


point = 0

gameon = True
isball = True
pause = False

W_Width = 800
W_Height = 1000
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"22101221_Circle Shooter Game")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)


glutMainLoop()