from __future__ import annotations


class Object:
    objects = []
    objectsWithTexture = []
    objectsWithBamp = []
    objectsWithGlobalVariables = []
    setNameTexture = set()

    def __init__(self, sdf: str, material: str):
        self.sdf = sdf
        self.material = material
        self.changePosition = None
        self.changeRotation = None
        self.nameTexture = None
        self.paramTexture = None
        self.nameBampTexture = None
        self.paramBamp = None
        self.globalVariables = None
        self.globalVariablesSet = None
        self.iD = len(Object.objects)
        Object.objects.append(self)

    def getId(self) -> int:
        return self.iD

    def setChangePosition(self, changePosition: str) -> Object:
        self.changePosition = changePosition
        return self

    def getChangePosition(self) -> str:
        return self.changePosition

    def isChangePosition(self) -> bool:
        return self.changePosition is not None

    def setChangeRotation(self, changeRotation: str) -> Object:
        self.changeRotation = changeRotation
        return self

    def getChangeRotation(self) -> str:
        return self.changeRotation

    def isChangeRotation(self) -> bool:
        return self.changeRotation is not None

    def getSdf(self) -> str:
        return self.sdf

    def getMaterial(self) -> str:
        return self.material

    def setTexture(self, nameTexture: str, param: str) -> Object:
        self.nameTexture = nameTexture
        self.paramTexture = param
        Object.objectsWithTexture.append(self)
        Object.setNameTexture.add(nameTexture)
        return self

    def isTexture(self) -> bool:
        return self.nameTexture is not None

    def getNameTexture(self) -> str:
        name = self.nameTexture.split('\\')[-1]
        return name

    def getParamTexture(self) -> str:
        return self.paramTexture

    def setBamp(self, nameTexture: str,
                param: str) -> Object:
        self.nameBampTexture = nameTexture
        self.paramBamp = param
        Object.objectsWithBamp.append(self)
        Object.setNameTexture.add(nameTexture)
        return self

    def getParamBamp(self) -> str:
        return self.paramBamp

    def isBamp(self) -> bool:
        return self.nameBampTexture is not None

    def getNameBampTexture(self) -> str:
        return self.nameBampTexture

    def setGlobalVariables(
            self, globalVariables: str,
            globalVariablesSet: str) -> Object:
        self.globalVariables = globalVariables
        self.globalVariablesSet = globalVariablesSet
        Object.objectsWithGlobalVariables.append(self)
        return self

    def getGlobalVariables(self) -> str:
        return self.globalVariables

    def getGlobalVariablesSet(self) -> str:
        return self.globalVariablesSet

    def isGlobalVariables(self) -> bool:
        return self.globalVariables is not None

    @staticmethod
    def getObjects() -> list[Object]:
        if len(Object.objects) == 0:
            raise RuntimeError("No object")

        return Object.objects

    @staticmethod
    def getObjectsWithTexture() -> list[Object]:
        if len(Object.objectsWithTexture) == 0:
            raise RuntimeError("No object")

        return Object.objectsWithTexture

    @staticmethod
    def getObjectsWithBamp() -> list[Object]:
        if len(Object.objectsWithBamp) == 0:
            raise RuntimeError("No object")

        return Object.objectsWithBamp

    @staticmethod
    def getSetNameTexture() -> set[str]:
        if len(Object.setNameTexture) == 0:
            raise RuntimeError("No Texture")

        return Object.setNameTexture

    @staticmethod
    def getObjectsWithGlobalVariables() -> list[Object]:
        if len(Object.objectsWithGlobalVariables) == 0:
            raise RuntimeError("No object")

        return Object.objectsWithGlobalVariables

    @staticmethod
    def clearObjects():
        Object.objects.clear()
        Object.objectsWithTexture.clear()
        Object.objectsWithBamp.clear()
        Object.setNameTexture.clear()
        Object.objectsWithGlobalVariables.clear()
