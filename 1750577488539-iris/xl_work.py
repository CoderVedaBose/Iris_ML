import pandas as pd

df = pd.read_csv("iris.data", header=None)

df.columns = [
    "sepal length",
    "sepal width",
    "petal length",
    "petal width",
    "class"
]

df.to_csv("output.csv", index=False)
