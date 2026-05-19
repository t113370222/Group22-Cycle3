import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. 讀取並立即過濾數據 (只拿需要的兩欄，減少記憶體負擔)
processed_path = os.path.join( 'data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_path, usecols=['SadOrHopeless', 'CurrentCigaretteUse'])

# 2. 預先計算四個核心數字 (這步最快)
# 分別計算兩組的成功次數(sum)與樣本數(count)
g1 = df[df['SadOrHopeless'] == 1]['CurrentCigaretteUse'].dropna()
g0 = df[df['SadOrHopeless'] == 0]['CurrentCigaretteUse'].dropna()

count1, n1 = g1.sum(), len(g1)
count0, n0 = g0.sum(), len(g0)
p1, p0 = count1/n1, count0/n0

# 3. 手動定義圖表與路徑
output_fig_dir = os.path.join('outputs', 'figures')
os.makedirs(output_fig_dir, exist_ok=True)

# --- 繪製兩張圖 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 圖 A: 比例長條圖 [cite: 135, 211]
ax1.bar(['Not Sad (0)', 'Sad (1)'], [p0, p1], color=['lightgrey', 'skyblue'])
ax1.set_title('Proportion of Cigarette Use')
ax1.set_ylabel('Proportion')

# 圖 B: 差異信賴區間 [cite: 138, 213]
diff = p1 - p0
se_diff = np.sqrt((p1*(1-p1)/n1) + (p0*(1-p0)/n0))
ci_low, ci_high = diff - 1.96*se_diff, diff + 1.96*se_diff

ax2.errorbar(x=[diff], y=[0], xerr=[[diff-ci_low], [ci_high-diff]], fmt='ro', capsize=10)
ax2.axvline(0, color='black', linestyle='--')
ax2.set_title('95% CI for Difference (p1 - p0)')
ax2.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_fig_dir, 'final_summary_plots.png'))
plt.show()

print(f"成功！樣本數：Sad組={n1}, 非Sad組={n0}")
print(f"差異信賴區間：[{ci_low:.4f}, {ci_high:.4f}]")

import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

# 1. 設定路徑與讀取資料
processed_path = os.path.join('data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_path)

# 2. 建立輸出資料夾 (依照要求存放在 outputs/tables)
output_table_dir = os.path.join('outputs', 'tables')
os.makedirs(output_table_dir, exist_ok=True)

# 3. 計算各組摘要數據
# Group 1: Felt Sad/Hopeless, Group 0: Did not feel Sad/Hopeless
summary = df.groupby('SadOrHopeless')['CurrentCigaretteUse'].agg(['count', 'sum', 'mean']).reset_index()
summary.columns = ['Group_Code', 'Sample_Size', 'Smoker_Count', 'Proportion']

# 4. 執行 Two-proportion z-test
# 提取成功次數與總次數
successes = summary['Smoker_Count'].values[::-1] # [Sad=1, Not Sad=0]
nobs = summary['Sample_Size'].values[::-1]

# 計算 z-stat 與 p-value
z_stat, p_value = sm.stats.proportions_ztest(successes, nobs)

# 計算比例差異與 95% 信賴區間
prop_diff = summary.loc[1, 'Proportion'] - summary.loc[0, 'Proportion']
conf_itv = sm.stats.confint_proportions_2indep(
    successes[0], nobs[0], successes[1], nobs[1], method='normal'
)

# 5. 整合為最終摘要表格
final_table = pd.DataFrame({
    'Metric': [
        'Sample Size (n)', 
        'Current Cigarette Use Proportion (p)', 
        'Difference in Proportions (p1 - p0)', 
        '95% CI for Difference', 
        'Z-statistic', 
        'P-value'
    ],
    'Group: Sad/Hopeless (1)': [
        int(summary.loc[1, 'Sample_Size']), 
        f"{summary.loc[1, 'Proportion']:.4f}", 
        f"{prop_diff:.4f}", 
        f"({conf_itv[0]:.4f}, {conf_itv[1]:.4f})", 
        f"{z_stat:.4f}", 
        f"{p_value:.4e}"
    ],
    'Group: Not Sad (0)': [
        int(summary.loc[0, 'Sample_Size']), 
        f"{summary.loc[0, 'Proportion']:.4f}", 
        "-", 
        "-", 
        "-", 
        "-"
    ]
})

# 6. 儲存表格
table_path_csv = os.path.join(output_table_dir, 'summary_table.csv')
final_table.to_csv(table_path_csv, index=False)

# 同時輸出 Markdown 格式方便您複製到報告或 README
print("\n--- Project Cycle 3 Summary Table ---")
print(final_table.to_markdown(index=False))

print(f"\n表格已儲存至: {table_path_csv}")