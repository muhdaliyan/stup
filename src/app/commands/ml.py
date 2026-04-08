"""stup ml — ML project with experiment tracking & MLflow."""

from app.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    write_file,
    run,
)

# ── Templates ────────────────────────────────────────────────────────

TRAIN_PY = '''\
"""Training script."""

import mlflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Example: load your data
# from data_loader import load_data


def train(config: dict):
    """Train a model with the given config."""
    mlflow.set_experiment(config.get("experiment_name", "default"))

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(config)

        # TODO: Replace with your model training logic
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        # model.fit(X_train, y_train)
        # predictions = model.predict(X_test)
        # accuracy = accuracy_score(y_test, predictions)

        # mlflow.log_metric("accuracy", accuracy)
        # mlflow.sklearn.log_model(model, "model")

        print("Training complete! Check MLflow UI: mlflow ui")


if __name__ == "__main__":
    config = {
        "experiment_name": "my-experiment",
        "learning_rate": 0.01,
        "epochs": 100,
        "batch_size": 32,
    }
    train(config)
'''

PREDICT_PY = '''\
"""Prediction / inference script."""

import mlflow


def predict(model_uri: str, data):
    """Load a model and make predictions."""
    model = mlflow.pyfunc.load_model(model_uri)
    return model.predict(data)


if __name__ == "__main__":
    # Example: load the latest model from MLflow
    # predictions = predict("models:/my-model/latest", test_data)
    print("Prediction script ready. Update with your model URI.")
'''

CONFIG_YAML = '''\
# Experiment configuration
experiment:
  name: my-experiment
  tracking_uri: ./mlruns

model:
  type: sklearn  # or pytorch
  hyperparameters:
    learning_rate: 0.01
    epochs: 100
    batch_size: 32

data:
  train_path: data/train.csv
  test_path: data/test.csv
  validation_split: 0.2
'''


def run_command() -> None:
    """Scaffold an ML project with experiment tracking."""
    print_banner("ml", "ML project with experiment tracking & MLflow")

    check_uv()
    ensure_venv_exists()

    # Install ML dependencies
    run("uv add scikit-learn torch mlflow")

    # Create directory structure
    create_dirs(
        "data",
        "models",
        "experiments/runs",
        "experiments/configs",
    )

    # Create files
    write_file("train.py", TRAIN_PY)
    write_file("predict.py", PREDICT_PY)
    write_file("experiments/configs/default.yaml", CONFIG_YAML)
    write_file("data/.gitkeep", "")
    write_file("models/.gitkeep", "")

    print_done()
