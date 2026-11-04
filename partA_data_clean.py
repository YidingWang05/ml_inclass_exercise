"""
ELEC70143 In-Class Exercise — Part A: missing values
1) 统计每个特征的缺失百分比
2) 查看缺失的"模式"（哪些列总是一起缺）
3) 处理策略：
   - 整套传感器都缺的行（9 个低成本传感器 + 温湿度全空）→ 删除
   - 只缺 NOx(GT) / NO2(GT) 的行 → 用 K 近邻 (KNN) 填补
4) 用"故意遮住已知值再填回去"的方法，检验 KNN 填补的准确度
"""
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

path = sys.argv[1] if len(sys.argv) > 1 else "data/q1.csv"
df = pd.read_csv(path)
TARGET = "CO(GT)"
features = [c for c in df.columns if c != TARGET]

# ---------- 1. 缺失百分比 ----------
print(f"数据形状: {df.shape}")
miss = (df.isna().mean() * 100).round(2).sort_values(ascending=False)
print("\n每列缺失百分比 (%):")
print(miss.to_string())
print(f"\n至少缺一个值的行: {df.isna().any(axis=1).sum()} "
      f"({df.isna().any(axis=1).mean()*100:.2f}%)")

# ---------- 2. 缺失模式 ----------
pattern = df[features].isna().apply(
    lambda r: ", ".join(r.index[r]) if r.any() else "(无缺失)", axis=1)
print("\n缺失模式 (哪些列同时缺失) 及行数:")
print(pattern.value_counts().to_string())

# ---------- 3. 处理 ----------
sensor_block = ["PT08.S1(CO)", "C6H6(GT)", "PT08.S2(NMHC)", "PT08.S3(NOx)",
                "PT08.S4(NO2)", "PT08.S5(O3)", "T", "RH", "AH"]
block_missing = df[sensor_block].isna().all(axis=1)
print(f"\n整套传感器缺失、将被删除的行: {block_missing.sum()} "
      f"({block_missing.mean()*100:.2f}%)")
df_clean = df.loc[~block_missing].reset_index(drop=True)

# KNN 需要先标准化，否则数值大的列(如 NOx 0-1500)会主导"距离"
# 注意：不把目标 CO(GT) 放进填补器，避免把答案泄露进特征
knn = make_pipeline(StandardScaler(), KNNImputer(n_neighbors=5, weights="distance"))
scaler = knn.named_steps["standardscaler"]
X_scaled_imp = knn.fit_transform(df_clean[features])
X_imp = pd.DataFrame(scaler.inverse_transform(X_scaled_imp), columns=features)
df_clean[features] = X_imp
print(f"处理后形状: {df_clean.shape}; 剩余缺失: {int(df_clean.isna().sum().sum())}")

# ---------- 4. 检验填补质量 ----------
# 在完整行里随机遮住 NOx(GT)/NO2(GT)，比较 KNN 与中位数填补的误差
rng = np.random.default_rng(0)
full = df.dropna().reset_index(drop=True)
print("\n填补质量检验 (随机遮住 10% 已知值后再填回):")
print(f"{'列':10s} {'KNN MAE':>10s} {'中位数 MAE':>12s} {'列标准差':>10s}")
for col in ["NOx(GT)", "NO2(GT)"]:
    idx = rng.choice(len(full), size=len(full) // 10, replace=False)
    masked = full[features].copy()
    truth = masked.loc[idx, col].copy()
    masked.loc[idx, col] = np.nan
    k = make_pipeline(StandardScaler(), KNNImputer(n_neighbors=5, weights="distance"))
    out = k.named_steps["standardscaler"].inverse_transform(k.fit_transform(masked))
    knn_mae = np.abs(out[idx, features.index(col)] - truth.values).mean()
    med_mae = np.abs(masked[col].median() - truth.values).mean()
    print(f"{col:10s} {knn_mae:10.1f} {med_mae:12.1f} {full[col].std():10.1f}")

df_clean.to_csv("q1_clean.csv", index=False)
print("\n已保存: q1_clean.csv")
