import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).with_name("iris.data")
MODEL_PATH = Path(__file__).with_name("model.joblib")


def train_and_save_model():
    df = pd.read_csv(DATA_PATH, header=None)
    df.columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]

    X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = df["species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(model, MODEL_PATH)
    return accuracy


if __name__ == "__main__":
    accuracy = train_and_save_model()
    print(f"Model trained successfully. Accuracy: {accuracy:.2%}")
