from model.modello import Model

myModel = Model()
myModel.buildGraph("France", 2015)
path, score = myModel.cammino_massimo(5)
print(path, score)