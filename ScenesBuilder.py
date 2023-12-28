from Scene import *


class ScenesBuilder:
    @staticmethod
    def __call__():
        fail = open("shader/scenesTextures_.glsl", "w")
        try:
            for scene in Scene.getScenes():
                if scene.getNameTextureIcon() is not None:
                    fail.write(f"uniform sampler2D {scene.getNameTextureIcon()};\n")

            fail.write("uniform sampler2D textureNotScenes;\n\n"
                       "vec3 getIconScene(int ID, vec2 uv) {\n"
                       "    switch (ID) {\n")

            for scene in Scene.getScenes():
                if scene.getNameTextureIcon() is not None:
                    fail.write(f"        case {scene.getId()}:\n")
                    fail.write(f"        return texture({scene.getNameTextureIcon()}, uv).rgb;\n")

            fail.write("        default:\n"
                       "        return texture(textureNotScenes, uv).rgb;\n"
                       "    }\n"
                       "}\n")
        finally:
            fail.close()




