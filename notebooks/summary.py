import pandas as pd
import os

# 1. 讀取之前的統計結果
table_path = os.path.join('outputs/tables/summary_table.csv')

if not os.path.exists(table_path):
    print("錯誤：找不到 summary_table.csv，請先執行製作表格的程式碼。")
else:
    # 讀取表格數據
    results = pd.read_csv(table_path)
    
    # 提取關鍵數值 (假設格式與之前產出的一致)
    n_sad = results.iloc[0, 1]
    n_not_sad = results.iloc[0, 2]
    p_sad = results.iloc[1, 1]
    p_not_sad = results.iloc[1, 2]
    diff = results.iloc[2, 1]
    ci = results.iloc[3, 1]
    p_val = results.iloc[5, 1]

    # 2. 建立輸出資料夾
    summary_dir = os.path.join('outputs', 'summary')
    os.makedirs(summary_dir, exist_ok=True)

    # 3. 撰寫總結內容
    summary_text = f"""# Project Cycle 3: Statistical Summary Report

## 1. Research Question
Is the proportion of current cigarette use different between students who felt sad or hopeless and those who did not? [cite: 83, 84]

## 2. Descriptive Comparison (Group Summaries)
- **Group 1 (Sad/Hopeless)**: n = {n_sad}, Proportion = {p_sad} [cite: 198, 199]
- **Group 0 (Not Sad)**: n = {n_not_sad}, Proportion = {p_not_sad} [cite: 198, 199]
- **Estimated Difference (p1 - p0)**: {diff} 

## 3. Inferential Results
- **95% Confidence Interval for Difference**: {ci} [cite: 201]
- **P-value**: {p_val} [cite: 203]
- **Statistical Method**: Two-proportion z-test [cite: 36, 42]

## 4. Final Interpretation in Context
Based on the analysis at alpha = 0.05[cite: 204]:
"""
    
    # 自動生成結論邏輯
    try:
        p_val_float = float(p_val)
        if p_val_float < 0.05:
            summary_text += f"- **Conclusion**: We reject the null hypothesis. There is a statistically significant difference in cigarette use between the two groups[cite: 204]. Students who felt sad or hopeless are more likely to use cigarettes[cite: 205]."
        else:
            summary_text += f"- **Conclusion**: We fail to reject the null hypothesis. There is no statistically significant difference in cigarette use between the two groups[cite: 204]."
    except:
        summary_text += "- **Conclusion**: (Please check P-value format and manually conclude based on alpha=0.05)."

    # 4. 存檔
    summary_file = os.path.join(summary_dir, 'Final_Summary.md')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print(f"總結報告已生成！請至以下路徑查看：\n{summary_file}")
    print("-" * 30)
    print(summary_text) 