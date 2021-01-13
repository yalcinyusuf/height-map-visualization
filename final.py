"""
Bilgisayar Grafikleri Final Projesi

Yusuf YALÇIN 18120205032

Yükseklik Haritası Görselleştirme 5.01.2021
"""
import noise
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import sys
from PIL import Image

#Random alan oluşturuken işimize yarıyor.
class Vector(object):

    def __init__(self, x, y, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

#Kamera için değişkenler
lx = 0.0
ly = 1.0
lz = -1.0
x1 = 0.0
y1 = 1.0
z1 = 5.0
#Dönüş açısı
angle = 0.0
angle1 = 0.40
X=60
# Gürültü yükseklik haritası hesaplaması için ölçek değişkeni
scale = 35.0

# Ağ(örgü) yüksekliği çarpanı anlamına gelen yükseklik ölçeği değişkeni.
height_scale = 10

# octaves, octaveOffsets, persistence ve lacunarity tümü çok katmanlı gürültü haritası için kullanılır.
octaves = 5 #oktaves, algoritmanın geçiş / katman sayısı anlamına gelir. Her geçiş daha fazla ayrıntı ekler.
octaveOffsets = []

persistence = 0.5 #Birbirini izleyen her değerin ne kadar fazlasını getirdiği anlamına gelir.
lacunarity = 2 #Kabaca geçiş başına eklenen ayrıntı düzeyidir.

# Ağ(örgü) yüksekliği yassılaştırma eşiğinden düşükse, ağ(örgü) yüksekliği 0 olacaktır.
flattening_threshold = 0.0125

# octave offsets üretmek.
for i in range(octaves):
    octaveOffsets.append(Vector(np.random.randint(-10000, 10000), np.random.randint(-10000, 10000)))

# Arazi genişliği ve yüksekliğinin boyutunu ayarlar.
terrain_size = 150

# Arazi yüksekliği verilerini depolar.
terrain = []

# Hareket offseti
offset = Vector(0, 0, 1)

# Köşeleri renklendirmek için manuel olarak hesaplanan değerler.
color_heights = [-0.7078, -0.6518, -0.5057, -0.27, -0.07, 0.1765, 0.3725, 0.5686, 0.9608]
# Texture id değişkenleri
id1 = 0
id2 = 0

# Texture işlemi yapar.
def LoadTexture(file):

    image = Image.open(file)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX")

    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    return id

# Gökyüzü çizdirir.
def drawSky():
    global terrain_size
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()

    glTranslatef(1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, id2)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex3f(0, terrain_size, -5)
    glTexCoord2f(0, 0)
    glVertex3f(0, terrain_size, 20)
    glTexCoord2f(1, 0)
    glVertex3f(terrain_size, terrain_size, 20)
    glTexCoord2f(1, 1)
    glVertex3f(terrain_size, terrain_size, -5)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, id2)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex3f(terrain_size, 0, -5)
    glTexCoord2f(0, 0)
    glVertex3f(terrain_size, 0, 20)
    glTexCoord2f(1, 0)
    glVertex3f(terrain_size, terrain_size, 20)
    glTexCoord2f(1, 1)
    glVertex3f(terrain_size, terrain_size, -5)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, id2)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex3f(0, 0, -5)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 20)
    glTexCoord2f(1, 0)
    glVertex3f(0, terrain_size, 20)
    glTexCoord2f(1, 1)
    glVertex3f(0, terrain_size, -5)
    glEnd()
    glPopMatrix()

    drawSun()
    glutSwapBuffers()
    glFlush()

# Güneş çizdirir
def drawSun():
    glColor3f(1.0, 0.75, 0)
    glTranslatef(-75.0, 0.0, 10.0)
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, id1)

    glBegin(GL_POLYGON)
    glTexCoord2f(0, 1)
    for i in range(0, 360):
        gunes_points1 = 10 * sin((i) * 3.14 / 180)
        gunes_points2 = 10 * cos((i) * 3.14 / 180)
        glVertex3f(gunes_points1 + terrain_size, terrain_size, gunes_points2 + 20)
    glTexCoord2f(0, 0)
    for i in range(0, 360):
        gunes_points1 = 10 * sin((i) * 3.14 / 180)
        gunes_points2 = 10 * cos((i) * 3.14 / 180)
        glVertex3f(gunes_points1 + terrain_size, terrain_size, gunes_points2 + 20)
    glTexCoord2f(1, 0)
    for i in range(0, 360):
        gunes_points1 = 10 * sin((i) * 3.14 / 180)
        gunes_points2 = 10 * cos((i) * 3.14 / 180)
        glVertex3f(gunes_points1 + terrain_size, terrain_size, gunes_points2 + 20)
    glTexCoord2f(1, 1)
    for i in range(0, 360):
        gunes_points1 = 10 * sin((i) * 3.14 / 180)
        gunes_points2 = 10 * cos((i) * 3.14 / 180)
        glVertex3f(gunes_points1 + terrain_size, terrain_size, gunes_points2 + 20)

    glEnd()

    glPopMatrix()
# Yükseklik değerine göre renk döndürür.
def getColor(value):
    global color_heights
    if value < color_heights[0]:
        return 42 / 255.0, 93 / 255.0, 186 / 255.0
    elif color_heights[0] <= value < color_heights[1]:
        return 51 / 255.0, 102 / 255.0, 195 / 255.0
    elif color_heights[1] <= value < color_heights[2]:
        return 207 / 255.0, 215 / 255.0, 127 / 255.0
    elif color_heights[2] <= value < color_heights[3]:
        return 91 / 255.0, 169 / 255.0, 24 / 255.0
    elif color_heights[3] <= value < color_heights[4]:
        return 63 / 255.0, 119 / 255.0, 17 / 255.0
    elif color_heights[4] <= value < color_heights[5]:
        return 89 / 255.0, 68 / 255.0, 61 / 255.0
    elif color_heights[5] <= value < color_heights[6]:
        return 74 / 255.0, 59 / 255.0, 55 / 255.0
    elif color_heights[6] <= value < color_heights[7]:
        return 250 / 255.0, 250 / 255.0, 250 / 255.0
    elif value >= color_heights[7]:
        return 1, 1, 1

# Çok katmanlı gürültü aracılığıyla araziyi hesaplar.
def calculate_terrain():
    global terrain
    terrain = []
    for y in range(terrain_size):
        terrain.append([])
        for x in range(terrain_size):
            terrain[-1].append(0)

    for y in range(terrain_size):
        for x in range(terrain_size):
            amplitude = 1
            frequency = 1
            noiseHeight = 0
            for i in range(octaves):
                sampleX = frequency * (x + octaveOffsets[i].x + offset.x) / scale
                sampleY = frequency * (y + octaveOffsets[i].y + offset.y) / scale
                noiseHeight += amplitude * noise.pnoise2(sampleX, sampleY)
                amplitude *= persistence
                frequency *= lacunarity
            terrain[x][y] = noiseHeight

    min_val = np.min(terrain)
    max_val = np.max(terrain)

    terrain = np.array(terrain)
    np.clip(terrain, -0.71, max_val)

# Klavyeden girilen w a s d tuşlarını algılar ve kamerayı hareket ettirir
def keyPressed(*args):
    global ly, lz, x1, y1, z1, angle1,X
    fraction = 1.0
    if args[0] == b"a" or args[0] == b"A":
        x1 -= 1
    elif args[0] == b"d" or args[0] == b"D":
        x1 += 1
    elif args[0] == b"w" or args[0] == b"W":
        lz = -cos(angle1)
        ly = sin(angle1)
        y1 += ly * fraction
        z1 += lz * fraction
    elif args[0] == b"s" or args[0] == b"S":
        lz = -cos(angle1)
        ly = sin(angle1)
        y1 -= ly * fraction
        z1 -= lz * fraction
    elif args[0] == b"r" or args[0] == b"R":
        X+=1
    elif args[0] == b"f" or args[0] == b"F":
        X-=1
    glutPostRedisplay()

# Klavyeden girilen ok tuşlarını algılar ve kamerayı hareket ettirir.
def processSpecialKeys(key, xx, yy):
    global lx, lz, x1, angle, ly, y1
    fraction = 1.0

    if key == GLUT_KEY_LEFT:
        angle -= 0.01
        lx = sin(angle)
        lz = -cos(angle)
    elif GLUT_KEY_RIGHT == key:
        angle += 0.01
        lx = sin(angle)
        lz = -cos(angle)
    elif GLUT_KEY_UP == key:
        x1 += lx * fraction
        y1 += ly * fraction
    elif GLUT_KEY_DOWN == key:
        x1 -= lx * fraction
        y1 -= ly * fraction

# Mouse tekerleğinden girdi alır ve kamera ile zoom yapmamızı sağlar.
def MouseWheel(*args):
    global lx, lz, x1, z1
    fraction = 1.0
    if args[1] == -1:
        x1 -= lx * fraction
        z1 -= lz * fraction
    elif args[1] == 1:
        x1 += lx * fraction
        z1 += lz * fraction
    else:
        pass
    glutPostRedisplay()

# Glut görüntüleme fonksiyonu
def display():

    # Clear Color ve Depth Buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Dönüşümleri sıfırla
    glLoadIdentity()
    # Kamerayı ayarlama
    gluLookAt(x1, y1, z1,
              x1 + lx, y1 , z1 + lz,
              0.0, 1.0, 0.0)

    #Arazi görüntüsü için çevirme ve döndürme
    glTranslatef(-terrain_size / 2.0, -25, -6)
    glRotate(X, -1, 0, 0)

    # triangles çizme
    glBegin(GL_TRIANGLES)
    for y in range(1, terrain_size - 1):
        for x in range(1, terrain_size - 1):
            if terrain[x][y + 1] < flattening_threshold:
                color = getColor(terrain[x][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex(x, (y + 1), 0)
            else:
                color = getColor(terrain[x][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, (y + 1), (terrain[x][y + 1] * height_scale))

            if terrain[x][y] < flattening_threshold:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, 0)

            else:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, (terrain[x][y] * height_scale))

            if terrain[x + 1][y + 1] < flattening_threshold:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), 0)
            else:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), (terrain[x + 1][y + 1] * height_scale))
    glEnd()

    # Daha fazla triangles çizme
    glBegin(GL_TRIANGLES)
    for y in range(1, terrain_size - 1):
        for x in range(1, terrain_size - 1):
            if terrain[x + 1][y + 1] < flattening_threshold:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), 0)
            else:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), (terrain[x + 1][y + 1] * height_scale))

            if terrain[x + 1][y] < flattening_threshold:
                color = getColor(terrain[x + 1][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), y, 0)
            else:
                color = getColor(terrain[x + 1][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), y, (terrain[x + 1][y] * height_scale))

            if terrain[x][y] < flattening_threshold:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, 0)
            else:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, (terrain[x][y] * height_scale))
    glEnd()

    glEnable(GL_TEXTURE_2D)

    drawSky()
    glDisable(GL_TEXTURE_2D)
    glFlush()

# Genel bir OpenGL başlatma fonksiyonu.
def initGL():
    calculate_terrain()
    global id1, id2
    glActiveTexture(GL_TEXTURE0)
    id1 = LoadTexture("yel.bmp")
    id2 = LoadTexture("bulut1.jpg")

    drawSky()
    drawSun()

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.780, 0.932, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

# Penceremiz yeniden boyutlandırıldığında çağrılır.
def changeSize(w, h):
    if (h == 0):
        h = 1
    ratio = 1.0 * w / h

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, w, h)
    gluPerspective(45, ratio, 1, 1000)
    glMatrixMode(GL_MODELVIEW)

# Ana Fonksiyon.
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(50, 50)
    glutCreateWindow("3D Terrain")

    glutDisplayFunc(display)
    glutReshapeFunc(changeSize)
    glutIdleFunc(display)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(processSpecialKeys)
    glutMouseWheelFunc(MouseWheel)
    glEnable(GL_DEPTH_TEST)
    initGL()
    glutMainLoop()

main()