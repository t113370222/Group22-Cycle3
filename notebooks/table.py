import pandas as pd
import numpy as np
import scipy.stats as stats
import os

# 1. 確保路徑與讀取已處理的檔案
processed_file = os.path.join('data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_file)

# 2. 建立兩個 Group 的複合反應變數 (根據清理後數據：1=Success/Yes, 0=Failure/No)
# Group A：既吃紅蘿蔔(1)又沒喝汽水(1)
df['Group_A_Diet'] = np.where((df['CarrotEating'] == 1) & (df['NoSodaDrinking'] == 0), 1, 0)

# Group B：既抽菸(1)又參加運動隊伍(1)
df['Group_B_Behavior'] = np.where((df['CurrentCigaretteUse'] == 1) & (df['SportsTeamParticipation'] == 1), 1, 0)

# 建立輸出資料夾
output_table_dir = os.path.join('outputs', 'tables')
os.makedirs(output_table_dir, exist_ok=True)

# 定義重複使用的統計檢定函式
def run_group_analysis(dataframe, response_var, group_title, filename):
    # 分組計算 (SadOrHopeless 1=有, 0=無)
    summary = dataframe.groupby('SadOrHopeless')[response_var].agg(['count', 'sum', 'mean']).reset_index()
    summary.columns = ['SadOrHopeless', 'Total_N', 'Success_Count', 'Proportion']
    
    # print(f"\n=================== {group_title} ===================")
    # print("--- 群體摘要表 ---")
    # print(summary.to_string(index=False))
    
    # 提取數值
    n1 = summary.loc[summary['SadOrHopeless'] == 1, 'Total_N'].values[0]
    x1 = summary.loc[summary['SadOrHopeless'] == 1, 'Success_Count'].values[0]
    p1 = summary.loc[summary['SadOrHopeless'] == 1, 'Proportion'].values[0]

    n0 = summary.loc[summary['SadOrHopeless'] == 0, 'Total_N'].values[0]
    x0 = summary.loc[summary['SadOrHopeless'] == 0, 'Success_Count'].values[0]
    p0 = summary.loc[summary['SadOrHopeless'] == 0, 'Proportion'].values[0]

    # Two-proportion z-test 計算
    p_pool = (x1 + x0) / (n1 + n0)
    z_stat = (p1 - p0) / np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n0))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% 信賴區間計算
    prop_diff = p1 - p0
    se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p0 * (1 - p0) / n0))
    lower = prop_diff - 1.96 * se_diff
    upper = prop_diff + 1.96 * se_diff

    # print("--- 統計推論結果 ---")
    # print(f"比例差異 (p1_Sad - p0_NotSad): {prop_diff:.4f}")
    # print(f"Z 檢定統計量: {z_stat:.4f}")
    # print(f"P 值: {p_value:.4e}")
    # print(f"95% 差異信賴區間: ({lower:.4f}, {upper:.4f})")
    
    # 建立最終表格並存檔
    final_table = pd.DataFrame({
        'Metric': ['Sample Size (n)', 'Success Proportion (p)', 'Difference (p1 - p0)', '95% CI', 'Z-statistic', 'P-value'],
        'Group: Sad (1)': [f"{n1}", f"{p1:.4f}", f"{prop_diff:.4f}", f"({lower:.4f}, {upper:.4f})", f"{z_stat:.4f}", f"{p_value:.4e}"],
        'Group: Not Sad (0)': [f"{n0}", f"{p0:.4f}", "-", "-", "-", "-"]
    })
    
    output_path = os.path.join(output_table_dir, filename)
    final_table.to_csv(output_path, index=False)
    print(f"💾 表格已儲存至: {output_path}")

# 3. 同時執行兩組行為的分析
run_group_analysis(df, 'Group_A_Diet', "Group A：飲食行為 (Carrot & Soda)", "summary_table_group_A.csv")
run_group_analysis(df, 'Group_B_Behavior', "Group B：風險行為 (Smoke & Sports)", "summary_table_group_B.csv")

