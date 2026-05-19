import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 確保路徑與讀取已處理的檔案
# 假設您剛才存檔的路徑如下
processed_file = os.path.join('data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_file)

# 2. 描述性統計：計算兩組的樣本數與成功比例 [cite: 198, 199]
# 分組：SadOrHopeless (1=有, 0=無)
# 反應變數：CurrentCigaretteUse (1=抽菸, 0=無)
summary_table = df.groupby('SadOrHopeless')['CurrentCigaretteUse'].agg(['count', 'sum', 'mean'])
summary_table.columns = ['Total_N', 'Smoker_Count', 'Proportion']
print("--- 群體摘要表 ---")
print(summary_table)

# 3. 執行 Two-proportion z-test [cite: 36, 42]
# 取得兩組的成功次數與總次數
successes = summary_table['Smoker_Count'].values
nobs = summary_table['Total_N'].values

# 執行檢定 (預設 alpha=0.05) [cite: 204]
z_stat, p_value = sm.stats.proportions_ztest(successes[::-1], nobs[::-1]) 
# [::-1] 是為了確保以 SadOrHopeless=1 作為第一組進行比較 [cite: 96, 97]

# 計算比例差異的信賴區間 [cite: 39, 201]
prop_diff = summary_table.loc[1, 'Proportion'] - summary_table.loc[0, 'Proportion']
conf_itv = sm.stats.confint_proportions_2indep(
    successes[1], nobs[1], successes[0], nobs[0]
)

print(f"\n--- 統計推論結果 ---")
print(f"比例差異 (p1 - p0): {prop_diff:.4f}")
print(f"Z 檢定統計量: {z_stat:.4f}")
print(f"P 值: {p_value:.4e}")
print(f"95% 差異信賴區間: ({conf_itv[0]:.4f}, {conf_itv[1]:.4f})")