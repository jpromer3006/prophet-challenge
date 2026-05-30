"""Prophet model training, persistence, and forecasting.

The public app loads a pre-trained model from ``models/prophet_model.joblib``
so page loads are instant. If that file is missing (e.g. first run on a fresh
checkout), it falls back to training from the cached data and saves the result.
"""

from pathlib import Path

import joblib
import pandas as pd
from prophet import Prophet

from data_loader import load_search_trends

MODEL_PATH = Path(__file__).parent / "models" / "prophet_model.joblib"


def _prophet_dataframe(trends: pd.DataFrame) -> pd.DataFrame:
    """Reshape the trends data into Prophet's required ``ds`` / ``y`` columns."""
    df = trends.reset_index()
    df.columns = ["ds", "y"]
    return df.dropna()


def train_model() -> Prophet:
    """Fit a Prophet model on the cached search-trend data and persist it."""
    df = _prophet_dataframe(load_search_trends())
    model = Prophet()
    model.fit(df)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model() -> Prophet:
    """Load the pre-trained model, retraining if it's missing or unreadable.

    A model pickled under one Prophet version can fail to unpickle under a
    different version on the host, so any load error falls back to a fresh fit
    rather than crashing the app.
    """
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass
    return train_model()


def forecast(model: Prophet, periods: int, freq: str = "h") -> pd.DataFrame:
    """Forecast ``periods`` steps beyond the training window."""
    future = model.make_future_dataframe(periods=periods, freq=freq)
    return model.predict(future)


if __name__ == "__main__":
    print("Training Prophet model on cached data...")
    train_model()
    print(f"Saved model to {MODEL_PATH}")
