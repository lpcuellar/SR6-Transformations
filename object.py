##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR6: TRANSFORMATIONS
##  LUIS PEDRO CUÉLLAR - 18220
##


import struct

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Object(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = [line for line in file.readlines() if line.strip()]

        self.vertices = []
        self.normals = []
        self.texture_coords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try :
                    prefix, value = line.split(' ', 1)
                except :
                    continue

                if prefix == 'v': # vertices
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'vt':
                    self.texture_coords.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                    if "//" in value:
                        self.faces.append([list(map(int,vert.split('//'))) for vert in value.split(' ')])

                    else:
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height) :
            self.pixels.append([])
            for x in range(self.width) :
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255

                self.pixels[y].append(color(r, g, b))

        image.close()

    def getColor(self, tx, ty):
        if (tx >= 0) and (tx <= 1) and (ty >= 0) and (ty <= 1) :
            x = int(tx * self.width - 1)
            y = int(ty * self.height - 1)

            return self.pixels[y][x]

        else :
            return color(0, 0, 0)
