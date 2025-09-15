def classification_metrics(y_true, y_pred, y_prob=None):
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, average_precision_score
    m = {}
    m["accuracy"] = float(accuracy_score(y_true, y_pred))
    try:
        m["f1"] = float(f1_score(y_true, y_pred, average="binary"))
    except Exception:
        m["f1"] = float(f1_score(y_true, y_pred, average="macro"))
    if y_prob is not None:
        try:
            m["auroc"] = float(roc_auc_score(y_true, y_prob))
            m["auprc"] = float(average_precision_score(y_true, y_prob))
        except Exception:
            pass
    return m
