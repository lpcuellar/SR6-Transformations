##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR5: Textures
##  LUIS PEDRO CUÉLLAR - 18220
##


import struct
import numpy as np
from numpy import cos, sin, tan

from object import Object
from mathGl import MathGl


##  char --> 1 byte
def char(var):
    return struct.pack('=c', var.encode('ascii'))

##  word --> 2 bytes
def word(var):
    return struct.pack('=h', var)

##  dword --> 4 bytes
def dword(var):
    return struct.pack('=l', var)

##  function that puts the rgb value of a color into bytes
def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Render(object):
    def __init__(self, width, height, background = None):
        self.glInit(width, height, background)
        self.current_color = color(1, 1, 1)

    ##  initiates the image with the width, height and background color
    def glInit(self, width, height, background):
        background = color(0, 0, 0) if background == None else background

        self.bg_color = background

        self.glCreateWindow(width, height)

        self.mathGl = MathGl()

        self.light = [0, 0, 1]
        self.current_texture = None
        self.current_shader = None

        self.createViewMatrix()
        self.createProjectionMatrix()

    ##  creates the window with the given
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear(self.bg_color)
        self.glViewPort(0, 0, width, height)

    def createViewMatrix(self, camera_position = [0, 0, 0], camera_rotation = [0, 0, 0]):
        camera_matrix = self.createObjectMatrix(translate = camera_position, rotate = camera_rotation)
        self.viewMatrix = self.mathGl.invert_matrix(camera_matrix)

    def lookAt(self, eye, camera_position = [0, 0, 0]):
        forward = self.mathGl.subtract(camera_position, eye)
        forward_norm = self.mathGl.norm(forward)

        for i in range(len(forward)) :
            forward[i] = forward[i] / forward_norm[i]

        right = self.mathGl.cross([0, 1, 0], forward)
        right_norm = self.mathGl.norm(right)

        for i in range(len(right)) :
            right[i] = right[i] = right[i] / right_norm[i]

        up = self.mathGl.cross([0, 1, 0], right)
        up_norm = self.mathGl.norm(up)

        for i in range(len(up)) :
            up[i] = up[i] / up_norm[i]

        camera_matrix = [ [right[0], up[0], forward[0], camera_position[0]],
                          [right[1], up[1], forward[1], camera_position[1]],
                          [right[2], up[2], forward[2], camera_position[2]],
                          [0, 0, 0, 1]]

        self.viewMatrix = self.mathGl.invert_matrix(camera_matrix)

    def createProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        t = tan((fov * np.pi / 180) / 2) * n
        r = t * self.vp_width / self.vp_height

        self.projectionMatrix = [ [n / r, 0, 0, 0],
                                  [0, n / t, 0, 0],
                                  [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
                                  [0, 0, -1, 0] ]

    ##  colors the image with the background color
    def glClear(self, bg_color):
        self.bg_color = bg_color
        self.pixels = [ [ self.bg_color for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

    ##  defines an area inside the window in which it can be drawn points and lines
    def glViewPort(self, x, y, width, height):
         self.vp_x = x
         self.vp_y = y
         self.vp_width = width
         self.vp_height = height

         self.viewPortMatrix = [ [width / 2, 0, 0, x + width / 2],
                                 [0, height / 2, 0, y + height / 2],
                                 [0, 0, 0.5, 0.4],
                                 [0, 0, 0, 1] ]

    ##   changes de background color of the image
    def glClearColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

        self.bg_color = color(self.r, self.g, self.b)

        self.glClear(self.bg_color)

    ##  draws a point in the image with the given NDC coordinates
    def glVertex(self, x, y):
        ver_x = int(((x + 1) * (self.vp_width / 2)) + self.vp_x)
        ver_y = int(((y + 1) * (self.vp_height / 2)) + self.vp_y)
        self.pixels[round(ver_y)][round(ver_x)] = self.current_color

    ##  draws a pint in the image with pixel coordinates
    def glVertex_coordinates(self, x, y):
        self.pixels[y][x] = self.current_color

    ##  changes the color of the points that can be drawn
    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    ##  draws a straight line from (x0, y0) to (x1, y1)
    def glLine(self, x0, y0, x1, y1):
        x0 = round(( x0 + 1) * (self.vp_width  / 2 ) + self.vp_x)
        x1 = round(( x1 + 1) * (self.vp_width  / 2 ) + self.vp_x)
        y0 = round(( y0 + 1) * (self.vp_height / 2 ) + self.vp_y)
        y1 = round(( y1 + 1) * (self.vp_height / 2 ) + self.vp_y)

        dx = x1 - x0
        dy = y1 - y0

        steep = abs(dy) > abs(dx)

        if steep :
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1 :
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep :
                self.glVertex_coordinates(y, x)
            else :
                self.glVertex_coordinates(x, y)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    ##  this function draws a line in between to pixel coordinates. Starts in (x0, y0) and ends in (x1, y1)
    def glLine_coordinates(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep :
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1 :
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        try :
            m = dy/dx
        except ZeroDivisionError:
            pass
        else :
            y = y0

            for x in range(x0, x1 + 1) :
                if steep :
                    self.glVertex_coordinates(y, x)
                else :
                    self.glVertex_coordinates(x, y)

                offset += m
                if offset >= limit :
                    y += 1 if y0 < y1 else -1
                    limit += 1

    # def transform(self, vertex, scale = [1, 1, 1], translate = [0, 0, 0]) :
    #     transformed =[  round(vertex[0] * scale[0] + translate[0]),
    #                     round(vertex[1] * scale[1] + translate[1]),
    #                     round(vertex[2] * scale[2] + translate[2])  ]
    #     return transformed

    def transform(self, vertex, vMatrix):
        augVertex = [vertex[0], vertex[1], vertex[2], 1]
        first_multiply = self.mathGl.matrix_multiply(self.viewPortMatrix, self.projectionMatrix)
        second_multiply = self.mathGl.matrix_multiply(first_multiply, self.viewMatrix)
        third_multiply = self.mathGl.matrix_multiply(second_multiply, vMatrix)
        transVertex = self.mathGl.matrix_multiply(third_multiply, augVertex)

        transVertex =  transVertex.tolist()[0]

        transVertex = [transVertex[0] / transVertex[3], transVertex[1] / transVertex[3], transVertex[2] / transVertex[3]]

        return transVertex

    def dirTransform(self, vertex, vMatrix):
        augVertex = [vertex[0], vertex[1], vertex[2], 0]
        transVertex = self.mathGl.matrix_multiply(vMatrix, augVertex)
        transVertex = transVertex.tolist()[0]

        transVertex = [transVertex[0], transVertex[1], transVertex[2]]

        return transVertex

    def createObjectMatrix(self, translate = [0, 0, 0], scale = [1, 1, 1], rotate = [0, 0, 0]):
        translateMatrix = [ [1, 0, 0, translate[0]],
                            [0, 1, 0, translate[1]],
                            [0, 0, 1, translate[2]],
                            [0, 0, 0, 1] ]

        scaleMatrix = [ [scale[0], 0, 0, 0],
                        [0, scale[1], 0, 0],
                        [0, 0, scale[2], 0],
                        [0, 0, 0, 1] ]

        rotationMatrix = self.createRotationMatrix(rotate)

        first = self.mathGl.matrix_multiply(translateMatrix, rotationMatrix)
        second = self.mathGl.matrix_multiply(first, scaleMatrix)

        return second

    def createRotationMatrix(self, rotate = [0, 0, 0]):
        pitch = rotate[0] * (np.pi / 180)
        yaw = rotate[1] * (np.pi / 180)
        roll = rotate[2] * (np.pi / 180)

        rotationX = [ [1, 0, 0, 0],
                      [0, cos(pitch), -sin(pitch), 0],
                      [0, sin(pitch), cos(pitch), 0],
                      [0, 0, 0, 1] ]

        rotationY = [ [cos(yaw), 0, sin(yaw), 0],
                      [0, 1, 0, 0],
                      [-sin(yaw), 0, cos(yaw), 0],
                      [0, 0, 0, 1] ]

        rotationZ = [ [cos(roll), -sin(roll), 0, 0],
                      [sin(roll), cos(roll), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1] ]

        first = self.mathGl.matrix_multiply(rotationX, rotationY)
        second = self.mathGl.matrix_multiply(first, rotationZ)

        return second

    ##  this function loads the model for it to be drawn
    def loadModel(self, filename, translate, scale, rotate):
        model = Object(filename)

        modelMatrix = self.createObjectMatrix(translate, scale, rotate)
        rotationMatrix = self.createRotationMatrix(rotate)

        for face in model.faces :
            count_vertices = len(face)
            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]

            v0 = self.transform(v0, modelMatrix)
            v1 = self.transform(v1, modelMatrix)
            v2 = self.transform(v2, modelMatrix)

            if count_vertices > 3 :
                v3 = model.vertices[face[3][0] - 1]
                v3 = self.transform(v3, modelMatrix)

            if self.current_texture :
                vt0 = model.texture_coords[face[0][1] - 1]
                vt1 = model.texture_coords[face[1][1] - 1]
                vt2 = model.texture_coords[face[2][1] - 1]

                if count_vertices > 3 :
                    vt3 = model.texture_coords[face[3][1] - 1]

            else :
                vt0 = [0, 0]
                vt1 = [0, 0]
                vt2 = [0, 0]
                vt3 = [0, 0]

            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]

            vn0 = self.dirTransform(vn0, rotationMatrix)
            vn1 = self.dirTransform(vn1, rotationMatrix)
            vn2 = self.dirTransform(vn2, rotationMatrix)

            if count_vertices > 3 :
                vn3 = model.normals[face[3][2] - 1]
                vn3 = self.dirTransform(vn3, rotationMatrix)

            self.triangle_barycentric_coordinates(v0, v1, v2, texture_coords = (vt0, vt1, vt2), normals = (vn0, vn1, vn2))

            if count_vertices > 3 :
                self.triangle_barycentric_coordinates(v0, v2, v3, texture_coords = (vt0, vt2, vt3), normals = (vn0, vn2, vn3))


    ##  this fucntion draws a polygon with the given coordinates
    def glDrawPolygon(self, poly):
        length = len(poly)

        for i in range(length) :
            p0 = poly[i]
            p1 = poly[(i + 1) % length]

            self.glLine_coordinates(p0[0], p0[1], p1[0], p1[1])

            for x in range(self.width) :
                for y in range(self.height) :
                    if self.evenOdd(poly, x, y) :
                        self.glVertex_coordinates(x, y)

    ##  this function checks if a point is inside the polygon
    ##  code used in this function is in https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule#Implementation
    def evenOdd(self, poly, x, y):
        length = len(poly)
        i = 0
        j = 0
        j = length - 1
        c = False

        for i in range(length) :
            if ((poly[i][1] > y) != (poly[j][1] > y)) and (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1])) :
                c = not c
            j = i
        return c

    ##  this function draws triangles with barycentric coordinates
    def triangle_barycentric_coordinates(self, A, B, C, intensity = 1, texture = None, texture_coords = ()):
        ## definding box limits
        minX = min(A[0], B[0], C[0])
        maxX = max(A[0], B[0], C[0])

        minY = min(A[1], B[1], C[1])
        maxY = max(A[1], B[1], C[1])

        for x in range(minX, maxX + 1) :
            for y in range(minY, maxY + 1) :
                if (x >= self.width) or (x < 0) or (y >= self.height) or (y < 0):
                    continue

                point = [x, y]
                u, v, w = self.mathGl.barycentric_coords(A, B, C, point)

                if (u >= 0) and (v >= 0) and (w >=0) :
                    z = A[2] * u + B[2] * v + C[2] * w

                    if z > self.zbuffer[y][x] and z <= 1 and z >= -1 :
                        if self.current_texture :
                            r, g, b = self.current_shader(
                            self,
                            verts = (A, B, C),
                            barycentric_coords = (u, v, w),
                            texture_coords = texture_coords,
                            normals = normals,
                            color = color(1, 1, 1)
                            )

                        else :
                            b, g, r = self.current_color

                        self.current_color = color(r, g, b)
                        self.glVertex_coordinates(x, y)
                        self.zbuffer[y][x] = z

    ##  this function is used to write the image into the file, and saves it
    def glFinish(self, filename):
        file = open(filename, 'wb')

        ##  file header --> 14 bytes
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))

        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        ##  image header --> 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        ##  pixels --> 3 bytes each

        for x in range(self.height) :
            for y in range(self.width) :
                file.write(self.pixels[x][y])

        file.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth, depth, depth))

        archivo.close()
