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
from shaders import phong, toon, static

render = Render(1000, 1000)

render.current_texture = Texture('./textures/model.bmp')
render.current_shader = phong

posModel = [0, 0, -5]

render.lookAt(posModel, [2, 2, 0])

render.loadModel('./models/model.obj', posModel, [1, 1, 1], [0, 0, 0])

render.glFinish('output.bmp')
