from Object import Object


class ObjectsBuilder:
    @staticmethod
    def __call__():
        fileMap = open("shader/map_.glsl", "w")
        try:
            for object_ in Object.getObjects():
                if object_.isBamp():
                    fileMap.write(
                        f"float objectDist{object_.getId()}_notBamp(vec3 position) {'{'}\n" +
                        object_.getSdf() +
                        "}\n\n")

                fileMap.write(f"float objectDist{object_.getId()}(vec3 position) {'{'}\n")

                fileMap.write(object_.getChangePosition()
                              if object_.getChangePosition() is not None else "")
                fileMap.write(object_.getChangeRotation()
                              if object_.getChangeRotation() is not None else "")

                if object_.isBamp():
                    fileMap.write(
                        f"    float result = objectDist{object_.getId()}_notBamp(position);\n"
                        f"    if (result < PROCESSING_DISTANCE_BAMP) {'{'}\n"
                        f"        vec2 e = vec2(EPSILON, 0.);\n"
                        f"        vec3 normal = normalize(vec3(objectDist{object_.getId()}"
                        f"_notBamp(position)) -\n"
                        f"                      vec3(objectDist{object_.getId()}"
                        f"_notBamp(position - e.xyy),\n"
                        f"                           objectDist{object_.getId()}"
                        f"_notBamp(position - e.yxy),\n"
                        f"                           objectDist{object_.getId()}"
                        f"_notBamp(position - e.yyx)));\n"
                        f"        result += bumpMapping({object_.getNameBampTexture()}"
                        f", position, normal, result, {object_.getParamBamp()});\n"
                        "    }\n"
                        "    return result;\n")
                else:
                    fileMap.write(object_.getSdf())

                fileMap.write("}\n\n")

            first = Object.getObjects()[0]
            range_ = list(map(lambda x: x.getId(), Object.getObjects()))
            fileMap.write("float map(vec3 position) {\n"
                          f"    float result = objectDist{first.getId()}(position);\n")
            for i in range_[1::]:
                fileMap.write(f"    result = min(result, objectDist{i}(position));\n")
            fileMap.write("    return result;\n}\n\n")

            fileMap.write("float map_iD(vec3 position) {\n"
                          f"    float dist = objectDist{first.getId()}(position);\n"
                          f"    float iD = {first.getId()};\n")
            for i in range_[1::]:
                fileMap.write("    {\n"
                              f"         float dist_ = objectDist{i}(position);\n"
                              f"         if (dist_ < dist) dist = dist_, iD = {i};\n"
                              "    }\n")
            fileMap.write("    return iD;\n}\n")
        finally:
            fileMap.close()

        fileTextures = open("shader/textures_.glsl", "w")
        try:
            for nameTexture in Object.getSetNameTexture():
                name = nameTexture.split('\\')[-1]
                fileTextures.write(f"uniform sampler2D {name};\n")
        except RuntimeError:
            pass
        finally:
            fileMap.close()

        material = open("shader/material_.glsl", "w")
        try:
            for object_ in Object.getObjects():
                material.write(f"vec3 objectDistColor{object_.getId()}"
                               "(vec3 rayPosition, vec3 normal, vec3 rayDerection) {\n")

                if object_.isChangePosition() and \
                        (object_.isTexture() or
                         "rayPosition" in object_.getMaterial()):
                    material.write(object_.getChangePosition().replace("position", "rayPosition"))

                if object_.isChangeRotation():
                    changeRotation = object_.getChangeRotation()
                    if object_.isTexture() or "normal" in object_.getMaterial():
                        material.write(changeRotation.replace("position", "normal"))
                    if object_.isTexture() or "rayPosition" in object_.getMaterial():
                        material.write(changeRotation.replace("position", "rayPosition"))

                if object_.isTexture() and "textureColor" in object_.getMaterial():
                    material.write(
                        f"    vec3 textureColor = triPlanar({object_.getNameTexture()}, "
                        f"rayPosition, normal, {object_.getParamTexture()});\n")

                material.write(object_.getMaterial())
                material.write("}\n\n")

            material.write(
                "vec3 getMaterial(vec3 rayPosition, float id, vec3 normal, vec3 rayDerection) {\n"
                "    vec3 material = vec3(0.);\n"
                "    switch (int(id)) {\n")

            for object_ in Object.getObjects():
                material.write(f"       case {object_.getId()}:\n"
                               f"           material = objectDistColor{object_.getId()}"
                               f"(rayPosition, normal, rayDerection);\n"
                               f"           break;\n")
            material.write("        }\n"
                           "    return material;\n"
                           "}\n\n")
        finally:
            material.close()

        globalVariables = open("shader/globalVariables_.glsl", "w")

        try:
            objects = Object.getObjectsWithGlobalVariables()

            for object_ in objects:
                globalVariables.write(
                    object_.getGlobalVariables())

            globalVariables.write(
                "void initGlobalVariables() {\n")
            for object_ in objects:
                globalVariables.write(
                    object_.getGlobalVariablesSet())
            globalVariables.write(
                "}\n")
        except RuntimeError:
            globalVariables.write(
                "void initGlobalVariables() {}\n")
        finally:
            globalVariables.close()
