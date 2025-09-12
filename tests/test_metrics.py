from src.metrics import classification_metrics
import numpy as np

def test_metrics_shapes():
    y_true = np.array([0,1,1,0])
    y_pred = np.array([0,1,0,0])
    y_prob = np.array([0.1,0.8,0.4,0.2])
    m = classification_metrics(y_true, y_pred, y_prob)
    assert "accuracy" in m and "f1" in m
