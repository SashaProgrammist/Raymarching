import moderngl_window as mglw
from moderngl_window import geometry
from math import *

from ScenesBuilder import *

X = 0
Y = 1
Z = 2


class Texture:
    def __init__(self, load, iD, name=''):
        self.load = load
        self.iD = iD
        self.name = name


class App(mglw.WindowConfig):
    window_size = 1600, 900
    resource_dir = 'shader'
    fullscreen = False
    title = "rayMarch"
    cursor = False
    aspect_ratio = None

    def __init__(self, **kwargs):
        ScenesBuilder()()
        Scene.callScene(17)

        super().__init__(**kwargs)
        self.quad = geometry.quad_fs()
        self.prog = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='fragment_shader.glsl')

        self.countsScenes = len(Scene.getScenes())
        self.set_uniform("countsScenes", self.countsScenes)

        self.sceneIconTextures = []
        self.sceneIconTextures.append(Texture(
            self.load_texture_2d("../textures/scenes/textureNotScenes.png"),
            0,
            "textureNotScenes"))
        self.set_uniform("textureNotScenes", 0)
        for scene in Scene.getScenes():
            if scene.getNameTextureIcon() is not None:
                self.sceneIconTextures.append(Texture(
                    self.load_texture_2d(
                        f"../textures/scenes/{scene.getNameTextureIcon()}.png"),
                    scene.getId(),
                    scene.getNameTextureIcon()
                ))
                self.set_uniform(scene.getNameTextureIcon(),
                                 scene.getId())

        self.sceneTextures = []
        self.resetSceneTextures()

        self.set_uniform('resolution', self.window_size)

        fail = open("start", 'r')
        try:
            self.rotation, self.positionCamera, self.speedSpeed = \
                map(lambda el: list(map(float, el.split(" ")[0:-1])), fail.readlines())
            self.speedSpeed = self.speedSpeed[0]
        except Exception as exception:
            print(exception)
            self.rotation = [0.0, 0.0, 0.0]
            self.positionCamera = [0.0, 0.0, 0.0]
            self.speedSpeed = 1
        finally:
            fail.close()

        self.rotationSpeed = [0.0, 0.0, 0.0]
        self.set_uniform('rotation', tuple(self.rotation))

        self.speed = [0.0, 0.0, 0.0]
        self.set_uniform('startPosition', tuple(self.positionCamera))

        self.speedRotation = 0.05

        self.mousePos = [0.5, 0.5]
        self.set_uniform("mousePos", tuple(self.mousePos))

        self.maxSteps = 1000
        self.set_uniform("maxSteps", self.maxSteps)

        self.isTab = False
        self.set_uniform("isTab", self.isTab)

        self.AA = 4
        self.set_uniform("AA", self.AA)

        self.positionSlider = 1
        self.set_uniform("positionSlider", self.positionSlider)

        self.isMoveSlider = False

        self.resize(*self.window_size)

    def resetSceneTextures(self):
        self.sceneTextures.clear()

        iD = self.countsScenes + 1
        try:
            for nameTexture in Object.getSetNameTexture():
                self.sceneTextures.append(Texture(
                    self.load_texture_2d("../textures/" +
                                         nameTexture +
                                         ".png"), iD))
                self.set_uniform(nameTexture.split('\\')[-1], iD)
                iD += 1
        except RuntimeError:
            pass

        # try:
        #     for object_ in Object.getObjectsWithBamp():
        #         self.sceneTextures.append(Texture(
        #             self.load_texture_2d("../textures/" +
        #                                  object_.getNameBampTexture() +
        #                                  ".png"), iD))
        #         self.set_uniform(object_.getNameBampTexture(), iD)
        #         iD += 1
        # except RuntimeError:
        #     pass

    def resetStableUniform(self):
        self.set_uniform('resolution', self.window_size)
        self.set_uniform("positionSlider", self.positionSlider)
        self.set_uniform("countsScenes", self.countsScenes)

        self.maxSteps = 100
        self.set_uniform("maxSteps", self.maxSteps)

        self.set_uniform("AA", self.AA)

        for icon in self.sceneIconTextures:
            self.set_uniform(icon.name, icon.iD)

    def resetScene(self):
        self.prog.release()

        self.prog = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='fragment_shader.glsl')

        self.resetStableUniform()
        self.resetSceneTextures()

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f"uniform: {u_name} - not in ")

    def resize(self, width: int, height: int):
        self.window_size = width, height
        self.set_uniform('resolution', self.window_size)

    def key_event(self, key, action, modifiers):
        actionModifies = (self.wnd.keys.ACTION_PRESS == action) * 2 - 1

        match key:
            case self.wnd.keys.NUMPAD_4:
                self.rotationSpeed[Z] -= self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_6:
                self.rotationSpeed[Z] += self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_8:
                self.rotationSpeed[Y] -= self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_2:
                self.rotationSpeed[Y] += self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_7:
                self.rotationSpeed[X] += self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_9:
                self.rotationSpeed[X] -= self.speedRotation * actionModifies

            case self.wnd.keys.NUMPAD_5:
                self.rotation[0] = 0.

            case self.wnd.keys.W:
                self.speed[X] += self.speedSpeed * actionModifies

            case self.wnd.keys.S:
                self.speed[X] -= self.speedSpeed * actionModifies

            case self.wnd.keys.D:
                self.speed[Y] += self.speedSpeed * actionModifies

            case self.wnd.keys.A:
                self.speed[Y] -= self.speedSpeed * actionModifies

            case self.wnd.keys.PAGE_UP:
                self.speed[Z] += self.speedSpeed * actionModifies

            case self.wnd.keys.PAGE_DOWN:
                self.speed[Z] -= self.speedSpeed * actionModifies

            case self.wnd.keys.Z:
                if self.wnd.keys.ACTION_PRESS == action:
                    self.speedSpeed *= 2
                    self.speed[X] *= 2
                    self.speed[Y] *= 2
                    self.speed[Z] *= 2

            case self.wnd.keys.X:
                if self.wnd.keys.ACTION_PRESS == action:
                    self.speedSpeed /= 2
                    self.speed[X] /= 2
                    self.speed[Y] /= 2
                    self.speed[Z] /= 2

            case self.wnd.keys.G:
                if self.wnd.keys.ACTION_PRESS == action:
                    fail = open("start", "w")
                    try:
                        for element in self.rotation:
                            fail.write(str(element) + ' ')
                        fail.write('\n')
                        for element in self.positionCamera:
                            fail.write(str(element) + ' ')
                        fail.write('\n')
                        fail.write(str(self.speedSpeed) + ' ')
                    finally:
                        fail.close()

            case self.wnd.keys.TAB:
                if self.wnd.keys.ACTION_PRESS == action:
                    self.isTab = not self.isTab

            case self.wnd.keys.J:
                if self.wnd.keys.ACTION_PRESS == action:
                    self.resetScene()

    def isMoseOnSlider(self) -> bool:
        if abs(self.mousePos[X] +
               0.5 * self.window_size[X] / self.window_size[Y] -
               0.4) >= 0.05:
            return False
        if abs(self.mousePos[Y]) >= 0.8:
            return False
        return True

    def isMoseOnSetting(self) -> bool:
        if abs(self.mousePos[X] +
               0.5 * self.window_size[X] / self.window_size[Y]) >= 0.5:
            return False
        if abs(self.mousePos[Y]) >= 0.9:
            return False
        return True

    def isMoseOnScenes(self) -> bool:
        if abs(self.mousePos[X] +
               0.5 * self.window_size[X] / self.window_size[Y] +
               0.1) >= 0.35:
            return False
        if abs(self.mousePos[Y]) >= 0.8:
            return False
        return True

    def changeSlider(self):
        positionSlider = (self.mousePos[Y] / 0.7 + 1) / 2
        positionSlider = max(0, min(1, positionSlider))

        self.positionSlider = self.positionSlider * 0.8 + positionSlider * 0.2

    def mouse_press_event(self, x: int, y: int, button: int):
        self.setMosePos(x, y)
        if self.isTab and self.isMoseOnSlider():
            self.changeSlider()
            self.isMoveSlider = True

    def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
        self.setMosePos(x + dx, y + dy)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.setMosePos(x, y)

        if self.isTab and not self.isMoveSlider and self.isMoseOnScenes():
            shift = - 4 * self.mousePos[Y] + \
                    (1 - self.positionSlider) * max(self.countsScenes - 6, 0)
            louBorder = floor(2.2 + shift)
            upBorder = ceil(3 + shift)

            iD = louBorder + 1

            if iD < upBorder:
                Scene.callScene(iD)
                self.resetScene()

        self.isMoveSlider = False

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        self.setMosePos(x + dx, y + dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        if self.isTab and self.isMoseOnSetting():
            self.positionSlider += 0.25 * y_offset / (max(self.countsScenes - 6, 0))
            self.positionSlider = max(0, min(1, self.positionSlider))
            self.set_uniform("positionSlider", self.positionSlider)

    def setMosePos(self, x: int, y: int):
        y = self.window_size[Y] - y
        self.mousePos = [(2 * x - self.window_size[X]) / self.window_size[Y],
                         (2 * y - self.window_size[Y]) / self.window_size[Y]]

    def update(self, time, frame_time):
        self.rotation[Z] += self.rotationSpeed[Z] * cos(self.rotation[X]) + \
                            self.rotationSpeed[Y] * sin(self.rotation[X])
        self.rotation[Y] += self.rotationSpeed[Y] * cos(self.rotation[X]) - \
                            self.rotationSpeed[Z] * sin(self.rotation[X])
        if abs(self.rotation[Y]) > pi * 4 / 9:
            self.rotation[Y] = pi * 4 / 9 if self.rotation[Y] > 0 else -pi * 4 / 9
        self.rotation[X] += self.rotationSpeed[X]
        self.set_uniform('rotation', tuple(self.rotation))

        self.positionCamera[X] += self.speed[X] * cos(self.rotation[Z]) - \
                                  self.speed[Y] * sin(self.rotation[Z])
        self.positionCamera[Y] += self.speed[Y] * cos(self.rotation[Z]) + \
                                  self.speed[X] * sin(self.rotation[Z])
        self.positionCamera[Z] += self.speed[Z]
        self.set_uniform('startPosition', tuple(self.positionCamera))

        self.set_uniform("mousePos", tuple(self.mousePos))

        if frame_time != 0:
            maxSteps = max(min(self.maxSteps * 0.05 / frame_time, 10000), 100)
            self.maxSteps = (self.maxSteps * 10 + maxSteps) / 11
        self.set_uniform("maxSteps", int(self.maxSteps))

        self.set_uniform("isTab", self.isTab)

        if self.isMoveSlider:
            self.changeSlider()
            self.set_uniform("positionSlider", self.positionSlider)

    def render(self, time, frame_time):
        self.ctx.clear()
        self.update(time, frame_time)

        for texture in self.sceneTextures:
            texture.load.use(location=texture.iD)

        for texture in self.sceneIconTextures:
            texture.load.use(location=texture.iD)

        self.set_uniform('time', time)
        self.quad.render(self.prog)
