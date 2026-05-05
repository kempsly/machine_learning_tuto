# XGBoost Complete Tutorial
> **Master XGBoost from scratch** — theory, implementation, tuning, and production  
> Written for data scientists building ML pipelines

---

## Table of Contents

1. [What is XGBoost?](#1-what-is-xgboost)
2. [Installation](#2-installation)
3. [Your First XGBoost Model](#3-your-first-xgboost-model)
4. [Classification Problem](#4-classification-problem)
5. [Regression Problem](#5-regression-problem)
6. [Understanding the Data Matrix (DMatrix)](#6-understanding-the-data-matrix-dmatrix)
7. [All Important Parameters](#7-all-important-parameters)
8. [Early Stopping](#8-early-stopping)
9. [Cross Validation](#9-cross-validation)
10. [Feature Importance](#10-feature-importance)
11. [Handling Missing Values](#11-handling-missing-values)
12. [Handling Imbalanced Datasets](#12-handling-imbalanced-datasets)
13. [Hyperparameter Tuning — GridSearch](#13-hyperparameter-tuning--gridsearch)
14. [Hyperparameter Tuning — Optuna (recommended)](#14-hyperparameter-tuning--optuna-recommended)
15. [Sklearn Pipeline Integration](#15-sklearn-pipeline-integration)
16. [Multiclass Classification](#16-multiclass-classification)
17. [Custom Objective Function](#17-custom-objective-function)
18. [Model Saving and Loading](#18-model-saving-and-loading)
19. [SHAP Values — Explainability](#19-shap-values--explainability)
20. [XGBoost with GPU](#20-xgboost-with-gpu)
21. [Financial Use Case — Anomaly Detection](#21-financial-use-case--anomaly-detection)
22. [Financial Use Case — Credit Default Prediction](#22-financial-use-case--credit-default-prediction)
23. [Full Production Pipeline](#23-full-production-pipeline)
24. [Cheat Sheet](#24-cheat-sheet)

---

## 1. What is XGBoost?

XGBoost (eXtreme Gradient Boosting) is a **supervised machine learning algorithm** based on decision trees.
It wins most tabular data competitions (Kaggle) and is widely used in finance, fraud detection, and risk modeling.

### How it works — the core idea

Instead of building one big tree, XGBoost builds **many small trees sequentially**.
Each new tree focuses on correcting the mistakes of all previous trees.

```
Tree 1: makes predictions → has errors
Tree 2: learns from Tree 1's errors → has smaller errors
Tree 3: learns from Tree 2's errors → even smaller errors
...
Tree N: final prediction = sum of all trees
```

This process is called **Gradient Boosting** — each tree is fit on the **gradient** (direction of error) of the previous ensemble.

### XGBoost vs other algorithms

| Algorithm | Speed | Accuracy | Missing values | Overfitting control |
|---|---|---|---|---|
| **XGBoost** | ⚡ Fast | ⭐⭐⭐⭐⭐ | ✅ Built-in | ✅ Strong regularization |
| Random Forest | Medium | ⭐⭐⭐⭐ | ❌ Manual | ✅ Good |
| Decision Tree | Fast | ⭐⭐ | ❌ Manual | ❌ Poor |
| Linear Regression | Very fast | ⭐⭐ | ❌ Manual | ⚠️ Limited |
| Neural Network | Slow | ⭐⭐⭐⭐⭐ | ❌ Manual | ⚠️ Needs tuning |

### When to use XGBoost

✅ Tabular/structured data (CSV, Excel, SQL)  
✅ Classification (fraud, churn, default prediction)  
✅ Regression (price prediction, demand forecasting)  
✅ When you need feature importance  
✅ When interpretability matters (SHAP)  
✅ When training data has missing values  

❌ Images → use CNNs  
❌ Text → use Transformers  
❌ Time series with complex patterns → use LSTMs or Prophet  

---

## 2. Installation

```bash
# Cell 1 — Install XGBoost and dependencies
pip install xgboost scikit-learn pandas numpy matplotlib seaborn
pip install shap optuna                  # for explainability and tuning
pip install imbalanced-learn             # for imbalanced datasets
```

```python
# Cell 2 — Verify installation and check version
import xgboost as xgb
import sklearn
import numpy as np
import pandas as pd

print(f"XGBoost version  : {xgb.__version__}")
print(f"Scikit-learn     : {sklearn.__version__}")
print(f"NumPy            : {np.__version__}")
print(f"Pandas           : {pd.__version__}")
```

---

## 3. Your First XGBoost Model

```python
# Cell 3 — Simplest possible XGBoost model (classification)
import xgboost as xgb
from sklearn.datasets import load_breast_cancer    # binary classification dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ── Load data ────────────────────────────────────────────────
data = load_breast_cancer()
X, y = data.data, data.target
# X = 569 samples × 30 features (tumor measurements)
# y = 0 (malignant) or 1 (benign)

# ── Split into train and test ─────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% for testing
    random_state=42,      # reproducibility
    stratify=y,           # keep same class ratio in train/test
)

print(f"Train size : {X_train.shape}")
print(f"Test size  : {X_test.shape}")

# ── Train model ───────────────────────────────────────────────
model = xgb.XGBClassifier(
    n_estimators=100,     # number of trees
    random_state=42,
)

model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")    # typically ~0.97 on this dataset
```

---

## 4. Classification Problem

```python
# Cell 4 — Full classification pipeline with all metrics
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
import matplotlib.pyplot as plt
import seaborn as sns

# ── Data ─────────────────────────────────────────────────────
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model ─────────────────────────────────────────────────────
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42,
)

model.fit(X_train, y_train)

# ── Predictions ───────────────────────────────────────────────
y_pred      = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]   # probability of class 1

# ── All metrics ───────────────────────────────────────────────
print("=" * 45)
print("CLASSIFICATION METRICS")
print("=" * 45)
print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision : {precision_score(y_test, y_pred):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score  : {f1_score(y_test, y_pred):.4f}")
print(f"ROC AUC   : {roc_auc_score(y_test, y_pred_prob):.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=data.target_names))

# ── Confusion Matrix ──────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=data.target_names,
    yticklabels=data.target_names,
)
plt.title("Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.show()
```

### Understanding the metrics

| Metric | Formula | When it matters |
|---|---|---|
| **Accuracy** | correct / total | Balanced datasets |
| **Precision** | TP / (TP + FP) | When false positives are costly (spam filter) |
| **Recall** | TP / (TP + FN) | When false negatives are costly (fraud, cancer) |
| **F1 Score** | 2 × P × R / (P + R) | Imbalanced datasets |
| **ROC AUC** | Area under ROC curve | Overall ranking quality |

---

## 5. Regression Problem

```python
# Cell 5 — XGBoost for regression
import xgboost as xgb
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
import matplotlib.pyplot as plt

# ── Data ─────────────────────────────────────────────────────
data = fetch_california_housing()
X, y = data.data, data.target
# y = median house value in $100k units

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Model — regression uses XGBRegressor ─────────────────────
model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,        # L1 regularization
    reg_lambda=1.0,       # L2 regularization
    random_state=42,
)

model.fit(X_train, y_train)

# ── Predictions ───────────────────────────────────────────────
y_pred = model.predict(X_test)

# ── Regression metrics ────────────────────────────────────────
mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print("=" * 40)
print("REGRESSION METRICS")
print("=" * 40)
print(f"MAE  : {mae:.4f}")    # Mean Absolute Error — average error in same unit as y
print(f"MSE  : {mse:.4f}")    # Mean Squared Error — penalizes large errors more
print(f"RMSE : {rmse:.4f}")   # Root MSE — same unit as y, more interpretable
print(f"R²   : {r2:.4f}")     # 1.0 = perfect, 0.0 = predicts mean, <0 = worse than mean

# ── Actual vs Predicted plot ──────────────────────────────────
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.3, s=10)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         "r--", lw=2, label="Perfect prediction")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title(f"Actual vs Predicted (R²={r2:.3f})")
plt.legend()
plt.tight_layout()
plt.savefig("regression_plot.png", dpi=150)
plt.show()
```

---

## 6. Understanding the Data Matrix (DMatrix)

```python
# Cell 6 — DMatrix: XGBoost's native data format
# DMatrix is XGBoost's internal data structure
# It is faster and more memory-efficient than numpy arrays
# You should use it when: training on large datasets
#                         using the native xgb.train() API
#                         need to set feature names or weights

import xgboost as xgb
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

data = load_breast_cancer()
X, y = data.data, data.target
feature_names = list(data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Create DMatrix objects ────────────────────────────────────
dtrain = xgb.DMatrix(
    data=X_train,
    label=y_train,
    feature_names=feature_names,  # column names for importance plots
)

dtest = xgb.DMatrix(
    data=X_test,
    label=y_test,
    feature_names=feature_names,
)

print(f"DMatrix shape       : {dtrain.num_row()} rows × {dtrain.num_col()} cols")
print(f"Feature names count : {len(dtrain.feature_names)}")

# ── Train using native xgb.train() API ───────────────────────
# This is the low-level API — more control than XGBClassifier
params = {
    "objective":   "binary:logistic",   # binary classification
    "eval_metric": "logloss",
    "max_depth":   4,
    "eta":         0.1,                  # eta = learning rate in native API
    "subsample":   0.8,
    "seed":        42,
}

# watchlist monitors train AND test loss during training
watchlist = [(dtrain, "train"), (dtest, "eval")]

model = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=200,         # number of trees
    evals=watchlist,
    verbose_eval=50,             # print metrics every 50 rounds
)

# ── Predict ───────────────────────────────────────────────────
# native API returns probabilities directly
y_pred_prob = model.predict(dtest)
y_pred      = (y_pred_prob > 0.5).astype(int)

from sklearn.metrics import accuracy_score
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
```

---

## 7. All Important Parameters

```python
# Cell 7 — Complete parameter reference with explanations
import xgboost as xgb

# ── Tree booster parameters ───────────────────────────────────
model = xgb.XGBClassifier(

    # ── How many trees ────────────────────────────────────────
    n_estimators=300,
    # Number of boosting rounds (trees).
    # More trees → better fit but risk of overfitting.
    # Use early stopping to find the sweet spot.

    # ── Tree structure ────────────────────────────────────────
    max_depth=6,
    # Maximum depth of each tree (default=6).
    # Deeper = more complex = more overfitting risk.
    # Typical range: 3–10. Start with 4–6.

    min_child_weight=1,
    # Minimum sum of instance weight in a leaf.
    # Higher = more conservative = less overfitting.
    # Useful for imbalanced datasets.

    gamma=0,
    # Minimum loss reduction to make a split.
    # Higher = more conservative tree growth.
    # Range: 0–5.

    # ── Learning rate ─────────────────────────────────────────
    learning_rate=0.1,
    # Also called eta. Shrinks contribution of each tree.
    # Lower = more trees needed but better generalization.
    # Rule: lower learning_rate → higher n_estimators.
    # Typical: 0.01–0.3.

    # ── Sampling ──────────────────────────────────────────────
    subsample=0.8,
    # Fraction of training samples used per tree.
    # Adds randomness, reduces overfitting.
    # Range: 0.5–1.0.

    colsample_bytree=0.8,
    # Fraction of features used per tree.
    # Range: 0.5–1.0.

    colsample_bylevel=1.0,
    # Fraction of features used per tree level.

    colsample_bynode=1.0,
    # Fraction of features used per split.

    # ── Regularization ────────────────────────────────────────
    reg_alpha=0.0,
    # L1 regularization (Lasso).
    # Makes weights sparse — useful for many irrelevant features.
    # Range: 0–1.

    reg_lambda=1.0,
    # L2 regularization (Ridge) — default=1.
    # Smooths weights — reduces overfitting.
    # Range: 0–10.

    # ── Objective ─────────────────────────────────────────────
    objective="binary:logistic",
    # binary:logistic   → binary classification (returns probabilities)
    # multi:softmax     → multiclass (returns class labels)
    # multi:softprob    → multiclass (returns probabilities)
    # reg:squarederror  → regression (MSE)
    # reg:absoluteerror → regression (MAE)
    # rank:pairwise     → ranking

    # ── Evaluation metric ─────────────────────────────────────
    eval_metric="logloss",
    # logloss   → binary classification
    # mlogloss  → multiclass classification
    # error     → classification error rate
    # auc       → area under ROC curve
    # rmse      → regression
    # mae       → regression

    # ── Hardware ──────────────────────────────────────────────
    device="cpu",
    # "cpu"  → CPU training (default)
    # "cuda" → GPU training (requires CUDA)

    n_jobs=-1,
    # Number of CPU threads. -1 = use all available.

    random_state=42,
)

print("Model parameters:")
for k, v in model.get_params().items():
    print(f"  {k:25} = {v}")
```

---

## 8. Early Stopping

```python
# Cell 8 — Early stopping to prevent overfitting
# Problem: how do you know the right number of trees?
# Too few → underfitting (model doesn't learn enough)
# Too many → overfitting (model memorizes training data)
# Solution: early stopping — stop when validation metric stops improving

import xgboost as xgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Method 1 — sklearn API with eval_set ─────────────────────
model = xgb.XGBClassifier(
    n_estimators=1000,           # set high — early stopping will cut it
    learning_rate=0.05,
    max_depth=4,
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],   # validation set to monitor
    verbose=100,                 # print every 100 rounds
    early_stopping_rounds=50,    # stop if no improvement for 50 rounds
    # → best_ntree_limit is automatically set to the best round
)

print(f"\nBest iteration      : {model.best_iteration}")
print(f"Best validation score: {model.best_score:.4f}")

# ── Plot training curve ───────────────────────────────────────
results  = model.evals_result()
# results = {"validation_0": {"logloss": [0.5, 0.4, 0.3, ...]}}

train_loss = results["validation_0"]["logloss"]

plt.figure(figsize=(10, 5))
plt.plot(train_loss, label="Validation log loss")
plt.axvline(x=model.best_iteration, color="red", linestyle="--",
            label=f"Best iteration: {model.best_iteration}")
plt.xlabel("Boosting Round")
plt.ylabel("Log Loss")
plt.title("Early Stopping — Training Curve")
plt.legend()
plt.tight_layout()
plt.savefig("early_stopping.png", dpi=150)
plt.show()

# ── Method 2 — native API with callbacks ─────────────────────
dtrain = xgb.DMatrix(X_train, label=y_train)
dval   = xgb.DMatrix(X_val,   label=y_val)

params = {
    "objective":   "binary:logistic",
    "eval_metric": "logloss",
    "max_depth":   4,
    "eta":         0.05,
    "seed":        42,
}

model_native = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=1000,
    evals=[(dval, "val")],
    early_stopping_rounds=50,
    verbose_eval=100,
)

print(f"\nBest round  : {model_native.best_iteration}")
print(f"Best score  : {model_native.best_score:.4f}")
```

---

## 9. Cross Validation

```python
# Cell 9 — Cross validation for robust performance estimation
# Cross validation splits data into K folds
# Trains K models, each tested on a different fold
# Gives a more reliable estimate of real-world performance

import xgboost as xgb
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score, StratifiedKFold

data = load_breast_cancer()
X, y = data.data, data.target

# ── Method 1 — sklearn cross_val_score ───────────────────────
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# StratifiedKFold preserves class ratio in each fold
# crucial for imbalanced datasets

scores = cross_val_score(
    model, X, y,
    cv=cv,
    scoring="roc_auc",      # metric to evaluate
    n_jobs=-1,              # parallel
)

print("=" * 40)
print("5-FOLD CROSS VALIDATION")
print("=" * 40)
for i, s in enumerate(scores, 1):
    print(f"  Fold {i}: {s:.4f}")
print(f"\nMean  : {scores.mean():.4f}")
print(f"Std   : {scores.std():.4f}")
print(f"95% CI: [{scores.mean()-2*scores.std():.4f}, {scores.mean()+2*scores.std():.4f}]")

# ── Method 2 — native xgb.cv() with early stopping ───────────
dtrain = xgb.DMatrix(X, label=y)

params = {
    "objective":   "binary:logistic",
    "eval_metric": "auc",
    "max_depth":   4,
    "eta":         0.1,
    "seed":        42,
}

cv_results = xgb.cv(
    params=params,
    dtrain=dtrain,
    num_boost_round=500,
    nfold=5,                    # 5-fold CV
    stratified=True,            # stratified for classification
    early_stopping_rounds=30,
    verbose_eval=50,
    seed=42,
)

# cv_results is a DataFrame with mean and std of train/test metrics
print("\nCV Results (last 5 rounds):")
print(cv_results.tail())
print(f"\nBest round : {cv_results['test-auc-mean'].idxmax()}")
print(f"Best AUC   : {cv_results['test-auc-mean'].max():.4f} "
      f"± {cv_results.loc[cv_results['test-auc-mean'].idxmax(), 'test-auc-std']:.4f}")
```

---

## 10. Feature Importance

```python
# Cell 10 — Feature importance — understand what drives predictions
# XGBoost provides 3 types of feature importance:
# weight  : how many times a feature is used for splitting
# gain    : average improvement in loss from splits using this feature
# cover   : average number of samples affected by splits using this feature
# gain is the most meaningful for understanding predictive power

import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data = load_breast_cancer()
X, y = data.data, data.target
feature_names = list(data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ── Method 1 — built-in plot ──────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, importance_type in zip(axes, ["weight", "gain", "cover"]):
    xgb.plot_importance(
        model,
        importance_type=importance_type,
        ax=ax,
        max_num_features=10,     # top 10 features
        title=f"Feature Importance ({importance_type})",
    )

plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
plt.show()

# ── Method 2 — manual with pandas ────────────────────────────
importances = model.get_booster().get_score(importance_type="gain")

df_imp = (
    pd.DataFrame.from_dict(importances, orient="index", columns=["gain"])
    .reset_index()
    .rename(columns={"index": "feature"})
    .sort_values("gain", ascending=False)
)

print("Top 10 features by gain:")
print(df_imp.head(10).to_string(index=False))

# ── Method 3 — feature selection using importance threshold ──
# Remove features with 0 importance (never used by any tree)
used_features  = set(importances.keys())
all_features   = set([f"f{i}" for i in range(X.shape[1])])
unused_features = all_features - used_features
print(f"\nUnused features: {len(unused_features)}")
```

---

## 11. Handling Missing Values

```python
# Cell 11 — XGBoost handles missing values natively
# This is a major advantage over sklearn models
# XGBoost learns the best direction to go when a value is missing
# No need for imputation — the model itself handles it

import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X, y = data.data, data.target

# ── Artificially introduce missing values ─────────────────────
X_missing = X.copy().astype(float)
np.random.seed(42)
mask = np.random.rand(*X_missing.shape) < 0.15   # 15% missing at random
X_missing[mask] = np.nan

print(f"Missing values: {np.isnan(X_missing).sum():,} "
      f"({np.isnan(X_missing).mean():.1%})")

# ── Split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_missing, y, test_size=0.2, random_state=42
)

# ── XGBoost handles NaN automatically — no preprocessing needed
model = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_train, y_train)    # NaN values are fine here

y_pred = model.predict(X_test)
print(f"Accuracy with 15% missing: {accuracy_score(y_test, y_pred):.4f}")

# Compare with no missing values
model_full = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
X_train_full, X_test_full, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)
model_full.fit(X_train_full, y_train)
y_pred_full = model_full.predict(X_test_full)
print(f"Accuracy with no missing  : {accuracy_score(y_test, y_pred_full):.4f}")
# Accuracy drop is usually small — XGBoost is robust to missing values
```

---

## 12. Handling Imbalanced Datasets

```python
# Cell 12 — Imbalanced datasets — very common in finance
# Example: 99% normal transactions, 1% fraud
# A model that always predicts "normal" gets 99% accuracy but is useless
# Solutions: scale_pos_weight, class weights, SMOTE

import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE

# ── Create imbalanced dataset (1% positive = fraud) ──────────
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    weights=[0.99, 0.01],      # 99% class 0, 1% class 1
    random_state=42,
)

print(f"Class 0 (normal) : {(y==0).sum():,} ({(y==0).mean():.1%})")
print(f"Class 1 (fraud)  : {(y==1).sum():,} ({(y==1).mean():.1%})")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Method 1 — scale_pos_weight (simplest, recommended) ──────
# scale_pos_weight = count(negative) / count(positive)
# tells XGBoost to penalize missing a positive class more
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight = neg / pos
print(f"\nscale_pos_weight = {scale_pos_weight:.1f}")

model_weighted = xgb.XGBClassifier(
    n_estimators=200,
    scale_pos_weight=scale_pos_weight,   # key parameter for imbalance
    max_depth=4,
    random_state=42,
)
model_weighted.fit(X_train, y_train)
y_pred_w = model_weighted.predict(X_test)

print("\n--- With scale_pos_weight ---")
print(classification_report(y_test, y_pred_w, target_names=["Normal", "Fraud"]))
print(f"ROC AUC: {roc_auc_score(y_test, model_weighted.predict_proba(X_test)[:,1]):.4f}")

# ── Method 2 — SMOTE (oversample minority class) ─────────────
# SMOTE creates synthetic samples of the minority class
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

print(f"\nAfter SMOTE: {(y_train_sm==0).sum()} normal, {(y_train_sm==1).sum()} fraud")

model_smote = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
model_smote.fit(X_train_sm, y_train_sm)
y_pred_sm = model_smote.predict(X_test)

print("\n--- With SMOTE ---")
print(classification_report(y_test, y_pred_sm, target_names=["Normal", "Fraud"]))
print(f"ROC AUC: {roc_auc_score(y_test, model_smote.predict_proba(X_test)[:,1]):.4f}")

# ── Recommendation ────────────────────────────────────────────
# For finance/fraud: use scale_pos_weight first (fast, no data augmentation)
# If still poor recall: try SMOTE
# Always use F1 and ROC AUC — not accuracy — for imbalanced data
```

---

## 13. Hyperparameter Tuning — GridSearch

```python
# Cell 13 — GridSearchCV — exhaustive search over parameter grid
# Tries every combination of parameters and picks the best one
# Downside: slow when grid is large (exponential combinations)
# Use for small grids (< 100 combinations)

import xgboost as xgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import pandas as pd

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ── Define parameter grid ─────────────────────────────────────
param_grid = {
    "n_estimators":   [100, 200, 300],
    "max_depth":      [3, 4, 6],
    "learning_rate":  [0.05, 0.1, 0.2],
    "subsample":      [0.8, 1.0],
    # Total combinations: 3×3×3×2 = 54 models × 5 folds = 270 fits
    # Add more params and it grows exponentially — use Optuna for large grids
}

model = xgb.XGBClassifier(random_state=42, n_jobs=-1)

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring="roc_auc",        # optimize for AUC
    cv=5,                     # 5-fold cross validation
    n_jobs=-1,                # parallel
    verbose=2,
    refit=True,               # retrain best model on full training set
)

grid_search.fit(X_train, y_train)

print("=" * 45)
print("GRID SEARCH RESULTS")
print("=" * 45)
print(f"Best params   : {grid_search.best_params_}")
print(f"Best CV score : {grid_search.best_score_:.4f}")

# ── Evaluate best model ───────────────────────────────────────
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f"Test accuracy : {accuracy_score(y_test, y_pred):.4f}")

# ── Show all results sorted ───────────────────────────────────
results = pd.DataFrame(grid_search.cv_results_)
results = results[["params", "mean_test_score", "std_test_score", "rank_test_score"]]
results = results.sort_values("rank_test_score")
print("\nTop 5 combinations:")
print(results.head().to_string(index=False))
```

---

## 14. Hyperparameter Tuning — Optuna (recommended)

```python
# Cell 14 — Optuna — smart Bayesian hyperparameter optimization
# Optuna learns from past trials to focus on promising regions
# Much faster than GridSearch for the same or better results
# Recommended for real projects

import xgboost as xgb
import optuna
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ── Define objective function ─────────────────────────────────
# Optuna calls this function many times with different params
# It tries to maximize the returned value (or minimize if you use direction="minimize")
def objective(trial):
    params = {
        "n_estimators":     trial.suggest_int("n_estimators", 100, 1000),
        "max_depth":        trial.suggest_int("max_depth", 3, 10),
        "learning_rate":    trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample":        trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "reg_alpha":        trial.suggest_float("reg_alpha", 1e-8, 1.0, log=True),
        "reg_lambda":       trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "gamma":            trial.suggest_float("gamma", 0.0, 1.0),
    }

    model = xgb.XGBClassifier(**params, random_state=42, n_jobs=-1)

    # 5-fold CV score for this set of params
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc", n_jobs=-1)
    return scores.mean()


# ── Run optimization ──────────────────────────────────────────
optuna.logging.set_verbosity(optuna.logging.WARNING)    # suppress verbose output

study = optuna.create_study(direction="maximize")       # maximize AUC
study.optimize(objective, n_trials=100, timeout=120)    # 100 trials or 2 minutes

print("=" * 45)
print("OPTUNA RESULTS")
print("=" * 45)
print(f"Best trial     : #{study.best_trial.number}")
print(f"Best AUC (CV)  : {study.best_value:.4f}")
print("\nBest parameters:")
for k, v in study.best_params.items():
    print(f"  {k:25} = {v}")

# ── Train final model with best params ────────────────────────
best_model = xgb.XGBClassifier(
    **study.best_params,
    random_state=42,
    n_jobs=-1,
)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

from sklearn.metrics import accuracy_score, roc_auc_score
print(f"\nTest accuracy  : {accuracy_score(y_test, y_pred):.4f}")
print(f"Test ROC AUC   : {roc_auc_score(y_test, best_model.predict_proba(X_test)[:,1]):.4f}")
```

---

## 15. Sklearn Pipeline Integration

```python
# Cell 15 — Sklearn Pipeline — chain preprocessing + XGBoost
# Pipelines prevent data leakage (scaler fitted only on train data)
# Make your code cleaner and easier to deploy
# Can be saved as a single object

import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report

data = load_breast_cancer()
X, y = data.data, data.target

# introduce some missing values to test the pipeline
X = X.astype(float)
np.random.seed(42)
X[np.random.rand(*X.shape) < 0.05] = np.nan

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Build pipeline ────────────────────────────────────────────
pipeline = Pipeline(steps=[

    # Step 1: fill missing values with median
    ("imputer", SimpleImputer(strategy="median")),

    # Step 2: scale features (optional for XGBoost but good practice)
    # XGBoost is tree-based — scaling doesn't affect split decisions
    # but helps if you switch to a linear model later
    ("scaler", StandardScaler()),

    # Step 3: XGBoost classifier
    ("xgb", xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
    )),
])

# ── Train and evaluate ────────────────────────────────────────
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(classification_report(y_test, y_pred))

# ── Cross validate the whole pipeline ────────────────────────
scores = cross_val_score(pipeline, X, y, cv=5, scoring="roc_auc", n_jobs=-1)
print(f"CV ROC AUC: {scores.mean():.4f} ± {scores.std():.4f}")

# ── Access model inside pipeline ─────────────────────────────
xgb_model = pipeline.named_steps["xgb"]
print(f"\nBest iteration: {xgb_model.n_estimators}")

# ── Save entire pipeline as one file ─────────────────────────
import joblib
joblib.dump(pipeline, "xgboost_pipeline.pkl")
print("Pipeline saved to xgboost_pipeline.pkl")
```

---

## 16. Multiclass Classification

```python
# Cell 16 — Multiclass classification (more than 2 classes)
import xgboost as xgb
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ── Data — 3 classes ─────────────────────────────────────────
data = load_iris()
X, y = data.data, data.target
class_names = data.target_names
# y = 0 (setosa), 1 (versicolor), 2 (virginica)

print(f"Classes: {class_names}")
print(f"Class distribution: {np.bincount(y)}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model — use multi:softprob to get probabilities ──────────
model = xgb.XGBClassifier(
    objective="multi:softprob",      # returns probabilities per class
    num_class=3,                     # number of classes
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
)

model.fit(X_train, y_train)

# ── Predict ───────────────────────────────────────────────────
y_pred      = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)
# y_pred_prob shape: (n_samples, n_classes)
# y_pred_prob[0] = [0.02, 0.15, 0.83] → class 2 most likely

print(classification_report(y_test, y_pred, target_names=class_names))

# ── Confusion matrix ─────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(7, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Multiclass Confusion Matrix")
plt.tight_layout()
plt.savefig("multiclass_cm.png", dpi=150)
plt.show()
```

---

## 17. Custom Objective Function

```python
# Cell 17 — Custom objective function
# Use when built-in objectives don't fit your business problem
# Example: in finance, missing a fraud costs 10x more than a false alarm
# You can encode this asymmetry directly into the loss function

import xgboost as xgb
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

X, y = make_classification(n_samples=5000, n_features=20,
                            weights=[0.95, 0.05], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ── Custom weighted logistic loss ────────────────────────────
# false negative cost (missing fraud) = 10x false positive cost
FN_WEIGHT = 10.0

def weighted_logloss(y_pred, dtrain):
    """
    Custom gradient and hessian for weighted binary cross-entropy.
    Penalizes false negatives (missing fraud) more than false positives.

    y_pred  : raw scores (before sigmoid)
    dtrain  : DMatrix with true labels

    Returns: gradient, hessian (both numpy arrays)
    """
    y_true = dtrain.get_label()
    prob   = 1.0 / (1.0 + np.exp(-y_pred))    # sigmoid

    # weight: positive class (fraud) gets FN_WEIGHT times more penalty
    weight = np.where(y_true == 1, FN_WEIGHT, 1.0)

    # gradient of weighted log loss
    grad = weight * (prob - y_true)

    # hessian (second derivative)
    hess = weight * prob * (1.0 - prob)

    return grad, hess


# ── Train with custom objective ───────────────────────────────
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest  = xgb.DMatrix(X_test,  label=y_test)

params = {
    "max_depth":       4,
    "eta":             0.1,
    "seed":            42,
    "disable_default_eval_metric": 1,   # needed for custom objective
}

model_custom = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=200,
    obj=weighted_logloss,         # pass custom objective here
    evals=[(dtest, "test")],
    verbose_eval=50,
)

# ── Predict — apply sigmoid manually (raw API returns raw scores) ──
raw_scores     = model_custom.predict(dtest)
y_pred_prob    = 1.0 / (1.0 + np.exp(-raw_scores))
y_pred         = (y_pred_prob > 0.5).astype(int)

print(f"ROC AUC (custom loss): {roc_auc_score(y_test, y_pred_prob):.4f}")

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, target_names=["Normal", "Fraud"]))
```

---

## 18. Model Saving and Loading

```python
# Cell 18 — Save and load models for production
import xgboost as xgb
import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ── Method 1 — XGBoost native format (.ubj) ──────────────────
# Best: preserves all XGBoost metadata, smallest file, fastest load
model.save_model("model.ubj")
model_loaded = xgb.XGBClassifier()
model_loaded.load_model("model.ubj")
print(f"Native format: {os.path.getsize('model.ubj')/1024:.1f} KB")
print(f"Accuracy: {accuracy_score(y_test, model_loaded.predict(X_test)):.4f}")

# ── Method 2 — JSON format (human readable) ──────────────────
# Good for: debugging, inspecting tree structure, versioning
model.save_model("model.json")
model_json = xgb.XGBClassifier()
model_json.load_model("model.json")
print(f"\nJSON format  : {os.path.getsize('model.json')/1024:.1f} KB")
print(f"Accuracy: {accuracy_score(y_test, model_json.predict(X_test)):.4f}")

# ── Method 3 — joblib (best for sklearn Pipelines) ───────────
# Use when model is part of a Pipeline with preprocessing steps
joblib.dump(model, "model.pkl")
model_pkl = joblib.load("model.pkl")
print(f"\nJoblib format: {os.path.getsize('model.pkl')/1024:.1f} KB")
print(f"Accuracy: {accuracy_score(y_test, model_pkl.predict(X_test)):.4f}")

# ── Saving and loading inside a FastAPI endpoint ──────────────
# Example of how to use in production:
#
# @app.on_event("startup")
# def load_model():
#     app.state.model = xgb.XGBClassifier()
#     app.state.model.load_model("model.ubj")
#
# @app.post("/predict")
# def predict(features: list[float]):
#     X = np.array(features).reshape(1, -1)
#     pred = app.state.model.predict(X)
#     return {"prediction": int(pred[0])}
```

---

## 19. SHAP Values — Explainability

```python
# Cell 19 — SHAP values — explain why the model made each prediction
# SHAP = SHapley Additive exPlanations
# Tells you: for this specific prediction, which features pushed it up or down?
# Essential for regulated industries like finance (model explainability is mandatory)
# pip install shap

import xgboost as xgb
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

data = load_breast_cancer()
X, y = data.data, data.target
feature_names = list(data.feature_names)

X_df = pd.DataFrame(X, columns=feature_names)    # SHAP works best with DataFrames

X_train, X_test, y_train, y_test = train_test_split(
    X_df, y, test_size=0.2, random_state=42
)

model = xgb.XGBClassifier(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ── Create SHAP explainer ─────────────────────────────────────
# TreeExplainer is the fastest for tree-based models
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
# shap_values[i, j] = contribution of feature j to prediction for sample i
# positive value = pushes prediction towards class 1
# negative value = pushes prediction towards class 0

print(f"SHAP values shape: {shap_values.shape}")  # (n_samples, n_features)

# ── Plot 1 — Summary plot (global feature importance) ────────
plt.figure()
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.title("Global Feature Importance (SHAP)")
plt.tight_layout()
plt.savefig("shap_summary_bar.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Plot 2 — Beeswarm plot (distribution of SHAP values) ─────
plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.title("SHAP Value Distribution")
plt.tight_layout()
plt.savefig("shap_beeswarm.png", dpi=150, bbox_inches="tight")
plt.show()

# ── Plot 3 — Explain a single prediction ─────────────────────
sample_idx = 0
print(f"\nPrediction for sample {sample_idx}: {model.predict(X_test.iloc[[sample_idx]])[0]}")
print(f"Probability: {model.predict_proba(X_test.iloc[[sample_idx]])[0, 1]:.4f}")

shap.waterfall_plot(
    shap.Explanation(
        values=shap_values[sample_idx],
        base_values=explainer.expected_value,
        data=X_test.iloc[sample_idx].values,
        feature_names=feature_names,
    )
)

# ── SHAP values as DataFrame ──────────────────────────────────
shap_df = pd.DataFrame(shap_values, columns=feature_names)
print("\nMean |SHAP| per feature:")
print(shap_df.abs().mean().sort_values(ascending=False).head(10))
```

---

## 20. XGBoost with GPU

```python
# Cell 20 — GPU acceleration (if you have an NVIDIA GPU)
# Speeds up training by 10–50x on large datasets
# Requires: NVIDIA GPU + CUDA + XGBoost compiled with GPU support

import xgboost as xgb
import numpy as np
import time
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# large dataset to see GPU benefit
X, y = make_classification(n_samples=200_000, n_features=100, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ── CPU training ──────────────────────────────────────────────
model_cpu = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    device="cpu",       # use CPU
    tree_method="hist", # histogram method — fast on CPU
    random_state=42,
)

start = time.time()
model_cpu.fit(X_train, y_train)
cpu_time = time.time() - start
print(f"CPU training time: {cpu_time:.1f}s")

# ── GPU training ──────────────────────────────────────────────
# Uncomment if you have a GPU:
#
# model_gpu = xgb.XGBClassifier(
#     n_estimators=300,
#     max_depth=6,
#     device="cuda",       # use GPU — replaces tree_method="gpu_hist" in old API
#     random_state=42,
# )
#
# start = time.time()
# model_gpu.fit(X_train, y_train)
# gpu_time = time.time() - start
# print(f"GPU training time: {gpu_time:.1f}s")
# print(f"Speedup: {cpu_time/gpu_time:.1f}x")

# ── Check GPU availability ────────────────────────────────────
try:
    test = xgb.XGBClassifier(device="cuda", n_estimators=1)
    test.fit([[1, 2], [3, 4]], [0, 1])
    print("GPU is available")
except Exception:
    print("No GPU available — using CPU")
```

---

## 21. Financial Use Case — Anomaly Detection

```python
# Cell 21 — Anomaly detection in financial transactions
# Using XGBoost as an anomaly scorer
# Real use case from Fins'AIght: flag unusual GL account entries

import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

np.random.seed(42)

# ── Generate synthetic financial transaction data ─────────────
n_normal = 9500
n_anomaly = 500    # 5% anomalies (unusual transactions)

# Normal transactions
normal = pd.DataFrame({
    "amount":          np.random.lognormal(mean=7, sigma=1.5, size=n_normal),
    "hour":            np.random.randint(8, 18, n_normal),     # business hours
    "day_of_week":     np.random.randint(0, 5, n_normal),      # weekdays
    "account_type":    np.random.choice(["GL_EXPENSE", "GL_REVENUE", "GL_ASSET"], n_normal),
    "num_approvals":   np.random.randint(1, 4, n_normal),
    "is_recurring":    np.random.choice([0, 1], n_normal, p=[0.3, 0.7]),
    "label":           0,   # normal
})

# Anomalous transactions (unusual patterns)
anomaly = pd.DataFrame({
    "amount":          np.random.lognormal(mean=12, sigma=2, size=n_anomaly),   # very large
    "hour":            np.random.choice([0, 1, 2, 22, 23], n_anomaly),         # odd hours
    "day_of_week":     np.random.choice([5, 6], n_anomaly),                    # weekends
    "account_type":    np.random.choice(["GL_EXPENSE", "GL_REVENUE", "GL_ASSET"], n_anomaly),
    "num_approvals":   np.random.randint(0, 2, n_anomaly),                     # few approvals
    "is_recurring":    np.random.choice([0, 1], n_anomaly, p=[0.9, 0.1]),      # non-recurring
    "label":           1,   # anomaly
})

df = pd.concat([normal, anomaly], ignore_index=True).sample(frac=1, random_state=42)
print(f"Dataset: {len(df)} transactions — {df['label'].sum()} anomalies ({df['label'].mean():.1%})")

# ── Feature engineering ───────────────────────────────────────
le = LabelEncoder()
df["account_type_enc"] = le.fit_transform(df["account_type"])

# amount features
df["amount_log"] = np.log1p(df["amount"])           # log-transform for skewed distribution
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
df["is_night"]   = ((df["hour"] < 7) | (df["hour"] > 20)).astype(int)

features = ["amount_log", "hour", "day_of_week", "account_type_enc",
            "num_approvals", "is_recurring", "is_weekend", "is_night"]

X = df[features].values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model ─────────────────────────────────────────────────────
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    scale_pos_weight=neg / pos,    # handle imbalance
    random_state=42,
)
model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred      = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]

print("\n" + "=" * 45)
print("ANOMALY DETECTION RESULTS")
print("=" * 45)
print(classification_report(y_test, y_pred, target_names=["Normal", "Anomaly"]))
print(f"ROC AUC: {roc_auc_score(y_test, y_pred_prob):.4f}")

# ── Score all transactions ────────────────────────────────────
df["anomaly_score"] = model.predict_proba(X)[:, 1]
df["predicted"]     = model.predict(X)

# show top 10 most suspicious
print("\nTop 10 most suspicious transactions:")
print(df.nlargest(10, "anomaly_score")[["amount", "hour", "day_of_week",
                                         "account_type", "anomaly_score"]].to_string(index=False))
```

---

## 22. Financial Use Case — Credit Default Prediction

```python
# Cell 22 — Credit default prediction
# Binary classification: will a client default on their loan?
# Classic banking use case — directly relevant to Natixis CIB

import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import shap

np.random.seed(42)
n = 15000

# ── Synthetic credit dataset ──────────────────────────────────
df = pd.DataFrame({
    "age":               np.random.randint(18, 75, n),
    "income":            np.random.lognormal(10.5, 0.8, n),
    "debt_to_income":    np.random.beta(2, 5, n),
    "credit_score":      np.random.randint(300, 850, n),
    "loan_amount":       np.random.lognormal(10, 1, n),
    "loan_term_months":  np.random.choice([12, 24, 36, 48, 60], n),
    "employment_years":  np.random.exponential(5, n).clip(0, 40),
    "num_late_payments": np.random.poisson(0.5, n),
    "num_credit_lines":  np.random.randint(1, 20, n),
    "loan_purpose":      np.random.choice(["home", "car", "education", "personal"], n),
})

# default probability based on features (realistic)
default_prob = (
    0.3
    - 0.0003 * df["credit_score"]
    + 0.4    * df["debt_to_income"]
    + 0.02   * df["num_late_payments"]
    - 0.005  * df["employment_years"]
    + 0.0    * np.random.normal(0, 0.1, n)  # noise
).clip(0.02, 0.95)

df["default"] = (np.random.rand(n) < default_prob).astype(int)
print(f"Default rate: {df['default'].mean():.1%}")

# ── Feature engineering ───────────────────────────────────────
le = LabelEncoder()
df["loan_purpose_enc"] = le.fit_transform(df["loan_purpose"])
df["loan_to_income"]   = df["loan_amount"] / df["income"]
df["monthly_payment"]  = df["loan_amount"] / df["loan_term_months"]
df["payment_to_income"] = df["monthly_payment"] / (df["income"] / 12)

features = [
    "age", "income", "debt_to_income", "credit_score",
    "loan_amount", "loan_term_months", "employment_years",
    "num_late_payments", "num_credit_lines", "loan_purpose_enc",
    "loan_to_income", "monthly_payment", "payment_to_income",
]

X = df[features].values
y = df["default"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model ─────────────────────────────────────────────────────
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=neg / pos,
    eval_metric="auc",
    early_stopping_rounds=30,
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=100,
)

# ── Evaluate ──────────────────────────────────────────────────
y_pred      = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=["No Default", "Default"]))
print(f"ROC AUC: {roc_auc_score(y_test, y_pred_prob):.4f}")

# ── Risk segmentation ─────────────────────────────────────────
df_test = pd.DataFrame(X_test, columns=features)
df_test["default_prob"] = y_pred_prob
df_test["risk_segment"] = pd.cut(
    df_test["default_prob"],
    bins=[0, 0.1, 0.3, 0.6, 1.0],
    labels=["Low", "Medium", "High", "Very High"],
)

print("\nRisk segmentation:")
print(df_test["risk_segment"].value_counts().sort_index())

# ── SHAP for regulatory compliance ────────────────────────────
# In finance, regulators require you to explain why a loan was rejected
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test[:100])  # explain 100 samples

shap.summary_plot(shap_values, X_test[:100], feature_names=features,
                  plot_type="bar", show=False)
plt.title("Credit Default — Feature Importance (SHAP)")
plt.tight_layout()
plt.savefig("credit_shap.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## 23. Full Production Pipeline

```python
# Cell 23 — Production-ready XGBoost pipeline
# Combines everything: preprocessing, training, evaluation, saving, prediction
# Plug this directly into FastAPI for serving

import xgboost as xgb
import numpy as np
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, roc_auc_score, f1_score,
    classification_report,
)
from sklearn.datasets import load_breast_cancer


class XGBoostProductionPipeline:
    """
    Production-ready XGBoost pipeline.
    Handles: training, evaluation, cross-validation,
             saving, loading, prediction, metadata tracking.
    """

    def __init__(self, model_name: str = "xgboost_model"):
        self.model_name  = model_name
        self.pipeline    = None
        self.metadata    = {}
        self.is_trained  = False

    def build_pipeline(self, xgb_params: dict = None) -> Pipeline:
        """Builds sklearn pipeline with preprocessing + XGBoost."""
        if xgb_params is None:
            xgb_params = {
                "n_estimators":     300,
                "max_depth":        4,
                "learning_rate":    0.05,
                "subsample":        0.8,
                "colsample_bytree": 0.8,
                "reg_alpha":        0.1,
                "reg_lambda":       1.0,
                "random_state":     42,
                "n_jobs":           -1,
            }

        self.pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler",  StandardScaler()),
            ("model",   xgb.XGBClassifier(**xgb_params)),
        ])
        return self.pipeline

    def train(self, X_train, y_train, feature_names: list = None):
        """Trains the pipeline and records metadata."""
        if self.pipeline is None:
            self.build_pipeline()

        self.pipeline.fit(X_train, y_train)
        self.is_trained = True
        self.feature_names = feature_names or [f"f{i}" for i in range(X_train.shape[1])]

        self.metadata.update({
            "model_name":      self.model_name,
            "trained_at":      datetime.now().isoformat(),
            "n_features":      X_train.shape[1],
            "n_train_samples": X_train.shape[0],
            "feature_names":   self.feature_names,
        })
        print(f"Model trained on {X_train.shape[0]:,} samples with {X_train.shape[1]} features")

    def evaluate(self, X_test, y_test) -> dict:
        """Evaluates model and returns all metrics."""
        y_pred      = self.pipeline.predict(X_test)
        y_pred_prob = self.pipeline.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy":  round(accuracy_score(y_test, y_pred), 4),
            "roc_auc":   round(roc_auc_score(y_test, y_pred_prob), 4),
            "f1_score":  round(f1_score(y_test, y_pred), 4),
        }

        self.metadata["test_metrics"] = metrics

        print("\n" + "=" * 40)
        print("EVALUATION RESULTS")
        print("=" * 40)
        for k, v in metrics.items():
            print(f"  {k:12} : {v}")
        print("\n" + classification_report(y_test, y_pred))

        return metrics

    def cross_validate(self, X, y, cv: int = 5) -> dict:
        """Runs stratified k-fold cross validation."""
        skf    = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        scores = cross_val_score(self.pipeline, X, y,
                                 cv=skf, scoring="roc_auc", n_jobs=-1)

        cv_results = {
            "mean_auc": round(scores.mean(), 4),
            "std_auc":  round(scores.std(), 4),
            "scores":   scores.round(4).tolist(),
        }

        self.metadata["cv_results"] = cv_results

        print(f"\n{cv}-Fold CV AUC: {scores.mean():.4f} ± {scores.std():.4f}")
        return cv_results

    def predict(self, X) -> np.ndarray:
        """Returns class predictions."""
        return self.pipeline.predict(X)

    def predict_proba(self, X) -> np.ndarray:
        """Returns class probabilities."""
        return self.pipeline.predict_proba(X)

    def save(self, output_dir: str = "."):
        """Saves pipeline and metadata."""
        os.makedirs(output_dir, exist_ok=True)
        model_path    = os.path.join(output_dir, f"{self.model_name}.pkl")
        metadata_path = os.path.join(output_dir, f"{self.model_name}_metadata.json")

        joblib.dump(self.pipeline, model_path)
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

        print(f"Model saved     : {model_path}")
        print(f"Metadata saved  : {metadata_path}")

    def load(self, output_dir: str = "."):
        """Loads pipeline and metadata."""
        model_path    = os.path.join(output_dir, f"{self.model_name}.pkl")
        metadata_path = os.path.join(output_dir, f"{self.model_name}_metadata.json")

        self.pipeline   = joblib.load(model_path)
        with open(metadata_path) as f:
            self.metadata = json.load(f)

        self.feature_names = self.metadata.get("feature_names", [])
        self.is_trained    = True
        print(f"Model loaded from {model_path}")
        print(f"Trained at: {self.metadata.get('trained_at')}")


# ── Usage ─────────────────────────────────────────────────────
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = list(data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train
pipe = XGBoostProductionPipeline("breast_cancer_model")
pipe.train(X_train, y_train, feature_names=feature_names)

# Cross validate
pipe.cross_validate(X, y, cv=5)

# Evaluate on test set
metrics = pipe.evaluate(X_test, y_test)

# Save
pipe.save("models/")

# Load and predict
pipe2 = XGBoostProductionPipeline("breast_cancer_model")
pipe2.load("models/")
predictions = pipe2.predict(X_test[:5])
probs       = pipe2.predict_proba(X_test[:5])[:, 1]

print("\nSample predictions:")
for i, (pred, prob) in enumerate(zip(predictions, probs)):
    print(f"  Sample {i}: class={pred}, prob={prob:.4f}")
```

---

## 24. Cheat Sheet

```python
# ── Install ───────────────────────────────────────────────────
# pip install xgboost scikit-learn shap optuna

# ── Import ────────────────────────────────────────────────────
import xgboost as xgb

# ── Classification ────────────────────────────────────────────
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=neg/pos,     # for imbalanced data
    eval_metric="auc",
    early_stopping_rounds=30,
    random_state=42,
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)
y_pred      = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]

# ── Regression ────────────────────────────────────────────────
model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ── Cross validation ──────────────────────────────────────────
from sklearn.model_selection import cross_val_score, StratifiedKFold
cv     = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
print(f"{scores.mean():.4f} ± {scores.std():.4f}")

# ── Save / load ───────────────────────────────────────────────
model.save_model("model.ubj")           # native (best)
model.save_model("model.json")          # human-readable
import joblib
joblib.dump(model, "model.pkl")         # for pipelines

model2 = xgb.XGBClassifier()
model2.load_model("model.ubj")

# ── SHAP ──────────────────────────────────────────────────────
import shap
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
shap.waterfall_plot(shap.Explanation(values=shap_values[0], ...))

# ── Optuna tuning ─────────────────────────────────────────────
import optuna
def objective(trial):
    params = {
        "n_estimators":  trial.suggest_int("n_estimators", 100, 1000),
        "max_depth":     trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
    }
    model = xgb.XGBClassifier(**params)
    return cross_val_score(model, X, y, cv=5, scoring="roc_auc").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)
print(study.best_params)

# ── Key parameters reference ──────────────────────────────────
# n_estimators      → number of trees (use early stopping)
# max_depth         → tree depth 3-10 (start at 4-6)
# learning_rate     → 0.01-0.3 (lower → more trees needed)
# subsample         → row sampling 0.5-1.0
# colsample_bytree  → column sampling 0.5-1.0
# scale_pos_weight  → neg/pos for imbalanced data
# reg_alpha         → L1 regularization (sparsity)
# reg_lambda        → L2 regularization (smoothness)
# min_child_weight  → conservative splits (higher = less overfit)
# gamma             → min loss reduction for split (higher = less overfit)

# ── Objective functions ───────────────────────────────────────
# binary:logistic   → binary classification
# multi:softprob    → multiclass
# reg:squarederror  → regression (MSE)
# reg:absoluteerror → regression (MAE)

# ── Eval metrics ─────────────────────────────────────────────
# logloss / mlogloss → classification loss
# error              → classification error rate
# auc                → ROC AUC
# rmse / mae         → regression
```

---

## Learning Path

```
Start here
    │
    ▼
Cell 3  → First model (get something running)
    │
    ▼
Cell 4  → Full classification metrics (learn to evaluate)
    │
    ▼
Cell 8  → Early stopping (avoid overfitting)
    │
    ▼
Cell 10 → Feature importance (understand your model)
    │
    ▼
Cell 9  → Cross validation (reliable performance estimate)
    │
    ▼
Cell 12 → Imbalanced data (real-world finance datasets)
    │
    ▼
Cell 14 → Optuna tuning (optimize for best performance)
    │
    ▼
Cell 19 → SHAP values (explain predictions)
    │
    ▼
Cell 22 → Credit default (Natixis use case)
    │
    ▼
Cell 23 → Production pipeline (deploy with FastAPI)
```

---

*XGBoost docs: https://xgboost.readthedocs.io*  
*SHAP docs: https://shap.readthedocs.io*  
*Optuna docs: https://optuna.readthedocs.io*  
*Scikit-learn docs: https://scikit-learn.org/stable/api*
