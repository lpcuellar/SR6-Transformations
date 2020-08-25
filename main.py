##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR6: TRANSFORMATIONS
##  LUIS PEDRO CUÉLLAR - 18220
##


from gl import Render, color
from object import Object, Texture
from shaders import *

render = Render(768, 432)
posModel = [0, 0, -3]

render.current_texture = Texture('./textures/model.bmp')
render.current_shader = phong

# HIGH ANGLE
print('high angle...')
render.lookAt(posModel, [0, 1.5, -0.7])
render.loadModel('./models/model.obj', posModel, [1, 1, 1], [0, 0, 0])
render.glFinish('high.bmp')
print('Terminado')

# MEDIUM ANGLE
render.glClear(color(0, 0, 0))
print('\nmedium angle...')
render.lookAt(posModel, [0, 0, -0.5])
render.loadModel('./models/model.obj', posModel, [1, 1, 1], [0, 0, 0])
render.glFinish('medium.bmp')
print('Terminado')

# LOW ANGLE
render.glClear(color(0, 0, 0))
print('\nlow angle...')
render.lookAt(posModel, [0, -1.2, -1])
render.loadModel('./models/model.obj', posModel, [1, 1, 1], [0, 0, 0])
render.glFinish('low.bmp')
print('Terminado')

# DUTCH ANGLE
render.glClear(color(0, 0, 0))
print('\ndutch angle...')
render.lookAt(posModel, [0, 0, -0.3])
render.loadModel('./models/model.obj', posModel, [1, 1, 1], [0, 0, 10])
render.glFinish('dutch.bmp')
print('Terminado')
