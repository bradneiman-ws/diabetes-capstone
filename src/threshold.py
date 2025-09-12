import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, roc_auc_score

def find_best_threshold(y_true, y_prob, metric="f1", step=0.01):
    """Grid search thresholds for binary probs to maximize a metric."""
    best_thr, best_score = 0.5, -1
    for thr in np.arange(0, 1+step, step):
        y_pred = (y_prob >= thr).astype(int)
        if metric == "f1":
            score = f1_score(y_true, y_pred)
        elif metric == "accuracy":
            score = accuracy_score(y_true, y_pred)
        elif metric == "precision":
            score = precision_score(y_true, y_pred)
        elif metric == "recall":
            score = recall_score(y_true, y_pred)
        elif metric == "roc_auc":
            try:
                score = roc_auc_score(y_true, y_prob)
            except Exception:
                score = -1
        else:
            raise ValueError(f"Unsupported metric: {metric}")
        if score > best_score:
            best_thr, best_score = thr, score
    return best_thr, best_score
