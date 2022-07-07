macroPad = []

class Button:
    def __init__(self):
        self.buttonName = ""
        self.buttonOperation = ""

    def SetButtonName(self, name):
        self.buttonName = name;

    def SetButtonOperation(self, operation):
        self.buttonOperation = operation

    def GetButtonName(self):
        return self.buttonName

    def GetButtonOperation(self):
        return self.buttonOperation


class MacroLayer:
    def __new__(cls):
        object = super().__new__(cls)
        return object

    def __init__(self):
        self.layername = ""
        self.buttonList = []
        for buttons in range(9):
            self.buttonList.append(Button())

    def __del__(self):
        layername = ""
        buttonList = []

    def SetUpButton(self, name, operation, index):
        self.buttonList[index].SetButtonName(name)
        self.buttonList[index].SetButtonOperation(operation)
    def SetupLayername(self, name):
        self.layername = name
    def GetLayerName(self):
        return self.layername
    def GetButtonName(self, index):
        return self.buttonList[index].GetButtonName()
    def GetButtonOperation(self, index):
        return self.buttonList[index].GetButtonOperation()

def ReadFromFile():
    buttonNameList = []
    buttonOperationsList = []
    layername = ""
    with open("config.txt", "r") as file:
        while True:
            inital = file.readline().strip()
            if(inital == '{'):
                layername = file.readline().strip()
                for x in range(9):
                    buttonname = file.readline().strip()
                    buttonOperation = file.readline().strip()
                    buttonNameList.append(buttonname)
                    buttonOperationsList.append(buttonOperation)
            elif(inital == '}'):
                layer = SetupLayer(layername, buttonNameList, buttonOperationsList)
                macroPad.append(layer)
                buttonNameList = []
                buttonOperationsList = []
                layername = ""
            elif (inital== ''):
                break

def GetMacroPadLayerLength():
    return len(macroPad)

def SetupLayer(layername, buttonNameList, ButtonOpList):
    layer = MacroLayer()
    layer.SetupLayername(layername)
    for x in range(len(buttonNameList)):
        layer.SetUpButton(buttonNameList[x], ButtonOpList[x], x)
    return layer

def ShowAll():
    for x in range(len(macroPad)):
        print(macroPad[x].GetLayerName())
        for j in range(len(macroPad[x].buttonList)):
            print(macroPad[x].GetButtonName(j))
