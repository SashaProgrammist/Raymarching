from __future__ import annotations

from ObjectsBuilder import *


class Scene:
    scenes = []

    def __init__(self, objects, nameTexture=None,
                 FOV=2, MAX_DISTANS=500.,
                 EPSILON=0.0001, PROCESSING_DISTANCE_BAMP=0.001,
                 BECK_GROUND="vec3(0.5,0.8, 0.9)"):
        self.objects = objects
        self.nameTextureIcon = nameTexture
        self.iD = len(Scene.scenes) + 1
        self.FOV = FOV
        self.MAX_DISTANS = MAX_DISTANS
        self.EPSILON = EPSILON
        self.PROCESSING_DISTANCE_BAMP = PROCESSING_DISTANCE_BAMP
        self.BECK_GROUND = BECK_GROUND
        Scene.scenes.append(self)

    def __call__(self):
        Object.clearObjects()
        self.objects()
        ObjectsBuilder()()

        fail = open("shader/scenesConst_.glsl", "w")
        try:
            fail.write(
                f"const float FOV = {self.FOV};\n"
                f"const float MAX_DISTANS = {self.MAX_DISTANS};\n"
                f"const float EPSILON = {self.EPSILON};\n"
                f"const float PROCESSING_DISTANCE_BAMP = "
                f"{self.PROCESSING_DISTANCE_BAMP};\n"
                f"const vec3 BECK_GROUND = {self.BECK_GROUND};")
        except Exception as exception:
            print(exception)
            fail.close()
            fail = open("shader/scenesConst_.glsl", "w")
            fail.write(
                "const float FOV = 2;\n"
                "const int MAX_STEPS = 1024;\n"
                "const float MAX_DISTANS = 500.;\n"
                "const float EPSILON = 0.0001;\n"
                "const float PROCESSING_DISTANCE_BAMP = 0.001;\n"
                "const vec3 BECK_GROUND = vec3(0.5,0.8, 0.9);\n")
        finally:
            fail.close()

    def getId(self):
        return self.iD

    def getNameTextureIcon(self):
        return self.nameTextureIcon

    @staticmethod
    def getScenes() -> list[Scene]:
        if len(Scene.scenes) == 0:
            raise RuntimeError

        return Scene.scenes

    @staticmethod
    def callScene(index):
        Scene.scenes[index]()


def scene1():
    Object("    return fSphere(position, 2);\n",
           "    return vec3(0.957, 0.957, 0.559);\n")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene2():
    Object("    return fSphere(position, 2);\n",
           "    return abs(normal);\n")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene3():
    Object("    return fSphere(position, 2);\n",
           "    return normalize(pow(abs(normal), vec3(1 + 4 * pow(sin(time), 2))));\n")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene4():
    Object("    return fSphere(position, 2);\n",
           "    return textureColor;\n"). \
        setTexture(
        "test3", "1")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene5():
    Object("    return fSphere(position, 2);\n",
           "    return textureColor;\n"). \
        setTexture(
        "test3", "1"). \
        setBamp(
        "test3Bamp", "0.01, 1")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene6():
    Object("    float dist = fPlane(position, vec3(0, 0, 1), 2);\n"
           "    vec3 pos = vec3(position.xy / 100, 10);\n"
           "    for (int i = 0; i < 10; i++) {\n"
           "        pos = mat * pos;\n\t\tdist -= "
           "pos.z * (noise(pos.xy));\n"
           "    }\n"
           "    return dist;\n",
           "    vec3 color = mix(vec3(0.,0.05, 0.08), vec3(0.035,0.349, 0.427), "
           "pow((reflect(-rayDerection, normal).z + 1) / 2, 2.));\n"
           "    return color;\n"). \
        setGlobalVariables(
        "mat3 mat;",
        "    mat2 _mat2 = rotationMatrix(time / 100);\n"
        "    mat[0].xy = _mat2[0] * 2.1;\n"
        "    mat[1].xy = _mat2[1] * 2.1;\n"
        "    mat[2].xyz = vec3(1 / 2.1);\n")


def scene7():
    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return min(sphere, box);\n",
           "    return vec3(0.4, 0.8, 0.7);\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return max(sphere, box);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.x -= 5;\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return max(sphere, -box);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.xz -= vec2(10, 2);\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return max(-sphere, box);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.xz -= vec2(10, -2);\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return fOpUnionRound(sphere, box, abs(sin(time)));\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.x -= 15;\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return fOpUnionColumns(sphere, box, 0.1, 10);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.x -= 20;\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return fOpUnionStairs(sphere, box, 0.4, 10);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.x -= 25;\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return fOpEngrave(sphere, box, 0.01);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.xz -= vec2(30, 2);\n")

    Object("    float sphere = fSphere(position, 1.3);\n"
           "    float box = fBox(position, vec3(1));\n"
           "    return fOpEngrave(box, sphere, 0.01);\n",
           "    return vec3(0.4, 0.8, 0.7);\n"). \
        setChangePosition(
        "    position.xz -= vec2(30, -2);\n")


def scene8():
    Object("    float distBox = fBox(position, vec3(2.5, 2.5, 3.));\n"
           "    float distBlob = fBlob(position - 1 * "
           "vec3(2 * sin(time * 5), 3 * sin(time * 4.8), 2.5 * sin(time * 2.89)));\n"
           "    float distPlane = fPlane(position, vec3(0, sin(time), cos(time)), 5);\n"
           "    return fOpUnionStairs(fOpTongue(distBox, distBlob,"
           " abs(2.5 * sin(time * 2.4584)), "
           "abs(2 * sin(time * 2.7548))), distPlane, 4, 10);\n",
           "    return textureColor;\n"). \
        setBamp(
        "test3Bamp", "0.01, 1"). \
        setChangePosition(
        "    position = position - vec3(0, 0, sin(time / 2.45));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n"). \
        setTexture(
        "test3", "1")


def scene9():
    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 0;\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 10;\n"
        "    position.z -= 10;\n"). \
        setChangeRotation(
        "    pR45(position.yz);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 10;\n"
        "    position.z += 10;\n"). \
        setChangeRotation(
        "    pR45(position.zy);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 20;\n"
        "    pMod1(position.z, 10 + sin(time) * 5);\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 30;\n"
        "    pModMirror1(position.z, 10 + sin(time) * 5);\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 40;\n"
        "    pModSingle1(position.z, 10 * sin(time));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 50;\n"
        "    pModInterval1(position.z, 10 * sin(time), "
        "-4 + sin(0.287*time), 4 + sin(0.428*time));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 60;\n"
        "    pR(position.yz, time);\n"
        "    pModPolar(position.yz, 10 + 5 * sin(time * 5));\n"
        "    position.y -= 20;\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 70;\n"
        "    pMod2(position.yz, vec2(10 + 3 * sin(time)));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 80;\n"
        "    pModMirror2(position.yz, vec2(10 + 3 * sin(time)));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 3.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 90;\n"
        "    pModGrid2(position.yz, vec2(10 + 3 * sin(time)));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox(position, vec3(2, 2.5, 30.));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 100;\n"
        "    pMirror(position.z, 10 + 3 * sin(time));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox2(position.xy, vec2(2, 2.5));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 110;\n"
        "    pMirrorOctant(position.yz, vec2(10 + 3 * sin(time)));\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")

    Object("    return fBox2(position.xy, vec2(2, 2.5));\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangePosition(
        "    position.x -= 130;\n"
        "    pReflect(position, "
        "normalize(vec3(sin(time), sin(time * 0.74), sin(time * 1.128))),"
        " 10);\n"). \
        setChangeRotation(
        "    pR(position.yz, time);\n")


def scene10():
    Object("    vec3 positionMod = position;\n"
           "    pMod3(positionMod, vec3(3.5));\n"
           "    float dist = max(-(length(positionMod) - 3 +"
           " length(position - startPosition) / 50),"
           " fBox(positionMod, vec3(2)));\n"
           "    return dist;\n",
           "    return vec3(0, 0.4, 0.8);\n")


def scene11():
    Object("    vec4 pos = vec4(position, 0);\n"
           "    pos = pos - vec4(1.1 * sin(time * 0.7481),\n"
           "                     1.2 * sin(time * 0.7),\n"
           "                     1.4 * sin(time * 0.69),\n"
           "                     1.3 * sin(time * 0.694));\n"
           "    pR(pos.zw, time);\n"
           "    pR(pos.wx, time * 1.2);\n"
           "    pR(pos.yw, time * 1.5);\n"
           "    vec4 d = abs(pos) - vec4(2);\n"
           "    return length(max(d, vec4(0))) + vmax(min(d, vec4(0))) - 0.5;\n",
           "    return vec3(0, 0.4, 0.8);\n")

    Object("    return fPlane(position, vec3(0,0,1), 5);\n",
           "    pModGrid2(rayPosition.xy, vec2(1 + 0.5 * sin(time)));\n"
           "    vec3 res = vec3(0);\n"
           "    bool a = abs(rayPosition.x) > 0.5;\n"
           "    bool b = abs(rayPosition.y) > 0.25;\n"
           "    if (a && b)\n"
           "        res = vec3(1);\n"
           "    if (a && !b)\n"
           "        res = vec3(0, 0.5, 1);\n"
           "    if (!a && b)\n"
           "        res = vec3(0, 0.5, 1);\n"
           "    if (!a && !b)\n"
           "        res = vec3(1, 0.5, 0);\n"
           "    return res;\n")


def scene12():
    Object("    float t = time;\n"
           "    vec4 pos = vec4(position, 0);\n"
           "    pos = pos - vec4(0, 1.2 * sin(t * 0.7),\n"
           "                        1.4 * sin(t * 0.69),\n"
           "                        1.3 * sin(t * 0.694));\n"
           "    pR(pos.zw, t);\n"
           "    pR(pos.wx, t * 1.2);\n"
           "    pR(pos.yw, t * 1.5);\n"
           "    pos = abs(pos) - vec4(2);\n"
           "    vec4 q = abs(pos + 0.1) - 0.1;\n"
           "    return -0.1 + min(min(min(min(min(\n"
           "        length(max(vec4(pos.x, pos.y, q.z, q.w), 0.0)) + "
           "min(vmax(vec4(pos.x, pos.y, q.z, q.w)), 0.0),\n"
           "        length(max(vec4(pos.x, q.y, pos.z, q.w), 0.0)) + "
           "min(vmax(vec4(pos.x, q.y, pos.z, q.w)), 0.0)),\n"
           "        length(max(vec4(pos.x, q.y, q.z, pos.w), 0.0)) + "
           "min(vmax(vec4(pos.x, q.y, q.z, pos.w)), 0.0)),\n"
           "        length(max(vec4(q.x, pos.y, pos.z, q.w), 0.0)) + "
           "min(vmax(vec4(q.x, pos.y, pos.z, q.w)), 0.0)),\n"
           "        length(max(vec4(q.x, pos.y, q.z, pos.w), 0.0)) + "
           "min(vmax(vec4(q.x, pos.y, q.z, pos.w)), 0.0)),\n"
           "        length(max(vec4(q.x, q.y, pos.z, pos.w), 0.0)) + "
           "min(vmax(vec4(q.x, q.y, pos.z, pos.w)), 0.0));\n",
           "        return vec3(0, 0.4, 0.8);\n")

    Object("    return fPlane(position, vec3(0,0,1), 5) + "
           "getSmus((position.x - 0.3) / 0.2) * 0.2;\n",
           "    vec3 res = vec3(1 - getSmus((rayPosition.x - 0.3) / 0.01) * 0.9);\n"
           "    return res;\n"). \
        setChangePosition(
        "    pMod2(position.xy, vec2(1));\n"
        "    pModPolar(position.xy, 8);\n")


def scene13():
    Object("	float k = 1.0;\n"
           "    for( int i=0; i<10; i++ ) {\n"
           "        position = (mm*vec4((abs(position)),1.0)).xyz;\n"
           "        k*= s;\n"
           "    }\n"
           "    float d = (length(position) - 0.25)/k;\n"
           "    return d;\n",
           "    return vec3(0, 0.4, 0.8);\n"). \
        setChangeRotation(
        "    pR(position.yz, 3.1415926535 / 2.);\n"). \
        setGlobalVariables(
        "mat4 mm;\n"
        "float s = 1.5;\n",
        "    float rtime = 45 + 0.01 * sin(time);\n"
        "    float _time = rtime;\n"
        "    _time += 15.0 * smoothstep(15.0, 25.0, rtime);\n"
        "    _time += 20.0 * smoothstep(65.0, 80.0, rtime);\n"
        "    _time += 35.0 * smoothstep(105.0, 135.0, rtime);\n"
        "    _time += 20.0 * smoothstep(165.0, 180.0, rtime);\n"
        "    _time += 40.0 * smoothstep(220.0, 290.0, rtime);\n"
        "    _time +=  5.0 * smoothstep(320.0, 330.0, rtime);\n"
        "    float time1 = (_time-10.0)*1.5 - 167.0;\n"
        "    float time2 = (_time-9.586)*1.48 - 124.0;\n"
        "    mm = rotationMat(vec3(1.4, 1.2, 3.4) + \n"
        "                     0.55*sin(0.1*vec3(0.40, 0.30, 0.61)*time1) + \n"
        "                     0.75*sin(0.1*vec3(0.58, 0.45, 0.48)*time2));\n"
        "    mm[0].xyz *= s;\n"
        "    mm[1].xyz *= s;\n"
        "    mm[2].xyz *= s;\n"
        "    mm[3].xyz = vec3(0.15, 0.05, -0.07) + \n"
        "                0.05 * sin(vec3(0.0, 1.0, 2.0) + 0.2 * \n"
        "                           vec3(0.31, 0.24, 0.42) * time1);\n")


def scene14():
    Object("    vec4 pos = vec4(position, 0);\n"
           "    pos = pos - vec4(0, 0.2 * sin(time * 0.7),\n"
           "                        0.4 * sin(time * 0.69),\n"
           "                        0.3 * sin(time * 0.694));\n"
           "    pR(pos.zw, time);\n"
           "    pR(pos.wx, time * 1.2);\n"
           "    pR(pos.yw, time * 1.5);\n"
           "    float x = abs(length(pos.xz) - 1);\n"
           "    float y = abs(length(pos.wy) - 1);\n"
           "    vec2 vec = vec2(x,y);\n"
           "    pR(vec, 3.1415926535 / 4. * time);\n"
           "    return length(vec) - 0.05;\n",
           "    return vec3(0, 0.4, 0.8);\n")


def scene15():
    Object("    vec4 pos = vec4(position, 0);\n"
           "    pos = pos - vec4(0, 1.2 * sin(time * 0.7),\n"
           "                        1.4 * sin(time * 0.69),\n"
           "                        1.3 * sin(time * 0.694));\n"
           "    pR(pos.zw, time);\n"
           "    pR(pos.wx, time * 1.2);\n"
           "    pR(pos.yw, time * 1.5);\n"
           "    float x = abs(length(pos.xz) - 1);\n"
           "    float y = abs(length(pos.wy) - 1);\n"
           "    vec2 vec = vec2(x,y);\n"
           "    pMod2(vec, vec2(3));\n"
           "    pR(vec, 3.1415926535 / 4. * time);\n"
           "    return length(vec) - 0.05;\n",
           "    return vec3(0, 0.4, 0.8);\n")


def scene16():
    n = 5

    for i in range(n):
        Object("    return fBox(position, vec3(0.5)) / 4;\n",
               "    if (abs(rayPosition.x) > abs(rayPosition.y) && abs(rayPosition.x) > abs(rayPosition.z)) \n"
               "        normal = vec3(sign(rayPosition.x), 0, 0);\n"
               "    else if (abs(rayPosition.y) > abs(rayPosition.x) && abs(rayPosition.y) > abs(rayPosition.z))"
               "        normal = vec3(0, sign(rayPosition.y), 0);\n"
               "    else\n"
               "        normal = vec3(0, 0, sign(rayPosition.z));\n"
               f"    return triPlanar(_{5 * 2 ** i}, rayPosition - vec3(0.5), normal, 1);\n"). \
            setChangeRotation("    pR(position.xy, time * 0.9 - timeFlight);\n"). \
            setChangePosition(
            f"    float timeFlight = length(position - startPosition) * {0.2 / 2 ** i};\n"
            "    vec2 pos = vec2(10, 0);\n"
            "    pR(pos, -time * 0.9 + timeFlight);\n"
            f"    position -= vec3(pos, {1.5 * i});\n"). \
            setTexture(f"scene16\\_{5 * 2 ** i}", "1")

    Object("    return fBox(position, vec3(0.5));\n",
           "    return triPlanar(inf, rayPosition - vec3(0.5), normal, 1);\n"). \
        setChangeRotation("    pR(position.xy, time * 0.9);\n"). \
        setChangePosition("    vec2 pos = vec2(10, 0);\n"
                          "    pR(pos, -time * 0.9);\n"
                          f"    position -= vec3(pos, {1.5 * n});\n"). \
        setTexture("scene16\\inf", "1")

    Object("    return fPlane(position, vec3(0, 0, 1), 2);\n",
           "    return vec3(0.585, 0.292, 0.0);\n")


def scene17():
    Object("    float scale = 1.0;\n"
           "\n"
           "	vec4 orb = vec4(1000.0); \n"
           "	\n"
           "	for( int i=0; i<8;i++ )	{\n"
           "		position = -1.0 + 2.0*fract(0.5*position+0.5);\n"
           "\n"
           "		float r2 = dot(position,position);\n"
           "		\n"
           "        orb = min( orb, vec4(abs(position),r2) );\n"
           "		\n"
           "		float k = (1.1 + 0.5*smoothstep( -0.3, 0.3, cos(0.1*time) ))/r2;\n"
           "		position *= k;\n"
           "		scale *= k;\n"
           "	}\n"
           "	\n"
           "	return 0.25*abs(position.z)/scale;\n",
           "    return vec3(0, 0.4, 0.8);")


def scene18():
    Object("    float timeFlight = time - length(position - startPosition) * 0.25;\n"
           "    vec4 pos = vec4(position, 0);\n"
           "    pos = pos - vec4(6,0,0,0);"
           "    pos = pos - vec4(1.1 * sin(timeFlight * 0.7481),\n"
           "                     1.2 * sin(timeFlight * 0.7),\n"
           "                     1.4 * sin(timeFlight * 0.69),\n"
           "                     1.3 * sin(timeFlight * 0.694));\n"
           "    pR(pos.zw, timeFlight);\n"
           "    pR(pos.wx, timeFlight * 1.2);\n"
           "    pR(pos.yw, timeFlight * 1.5);\n"
           "    vec4 d = abs(pos) - vec4(2);\n"
           "    return  0.25 * length(max(d, vec4(0))) + vmax(min(d, vec4(0)));\n",
           "    return vec3(0, 0.4, 0.8);\n")


def initScenes():
    Scene(scene1, "s1")
    Scene(scene2, "s2")
    Scene(scene3, "s3")
    Scene(scene4, "s4")
    Scene(scene5, "s5")
    Scene(scene6, "s6")
    Scene(scene7, "s7")
    Scene(scene8, "s8")
    Scene(scene9, "s9")
    Scene(scene10, "s10")
    Scene(scene11, "s11")
    Scene(scene12, "s12")
    Scene(scene13, "s13", EPSILON=0.0000001)
    Scene(scene14, "s14")
    Scene(scene15, "s15")
    Scene(scene16, "s16", EPSILON=0.01)
    Scene(scene17, "s17", EPSILON=0.0005)
    Scene(scene18, "s18")
