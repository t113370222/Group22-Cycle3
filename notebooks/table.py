import pandas as pd
import numpy as np
import scipy.stats as stats
import os

# 1. 讀取資料
processed_path = os.path.join('data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_path)

# 2. 建立輸出資料夾
output_table_dir = os.path.join('outputs', 'tables')
os.makedirs(output_table_dir, exist_ok=True)

# 3. 計算各組摘要數據 [cite: 173, 199]
summary = df.groupby('SadOrHopeless')['CurrentCigaretteUse'].agg(['count', 'sum', 'mean']).reset_index()
summary.columns = ['Group', 'n', 'successes', 'prop']

# 提取數值進行統計檢定 [cite: 198]
n1, p1 = summary.loc[1, 'n'], summary.loc[1, 'prop']
n0, p0 = summary.loc[0, 'n'], summary.loc[0, 'prop']
x1, x0 = summary.loc[1, 'successes'], summary.loc[0, 'successes']

# 4. 執行 Two-proportion z-test [cite: 42, 174, 202]
p_pool = (x1 + x0) / (n1 + n0)
z_stat = (p1 - p0) / np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n0))
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

# 5. 計算比例差異與 95% 信賴區間 [cite: 39, 200, 201]
diff = p1 - p0
se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p0 * (1 - p0) / n0))
lower = diff - 1.96 * se_diff
upper = diff + 1.96 * se_diff

# 6. 整合為最終摘要表格 [cite: 28, 193, 214]
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
        f"{n1:.0f}", f"{p1:.4f}", f"{diff:.4f}", 
        f"({lower:.4f}, {upper:.4f})", f"{z_stat:.4f}", f"{p_value:.4e}"
    ],
    'Group: Not Sad (0)': [
        f"{n0:.0f}", f"{p0:.4f}", "-", "-", "-", "-"
    ]
})

# 7. 儲存結果 [cite: 178]
output_path = os.path.join(output_table_dir, 'summary_table.csv')
final_table.to_csv(output_path, index=False)

# 8. 直接印出結果 (不使用 tabulate) [cite: 205]
print("\n--- Project Cycle 3 Summary Table ---")
print(final_table.to_string(index=False)) # 使用內建的 to_string 替代 to_markdown
print(f"\n表格已儲存至: {output_path}")