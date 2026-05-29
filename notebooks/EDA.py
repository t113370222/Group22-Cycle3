import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 確保路徑與讀取檔案
processed_file = os.path.join('data/processed/YRBS_2007_cleaned.csv')
df = pd.read_csv(processed_file)

# 2. 建立複合變數（更新：Group A 改為不喝汽水 NoSodaDrinking）
# CarrotEating == 1 (有吃紅蘿蔔) 且 SodaDrinking == 0 (代表沒喝汽水，即符合 NoSodaDrinking)
df['Group_A_Diet'] = np.where((df['CarrotEating'] == 1) & (df['NoSodaDrinking'] == 0), 1, 0)
df['Group_B_Behavior'] = np.where((df['CurrentCigaretteUse'] == 1) & (df['SportsTeamParticipation'] == 1), 1, 0)

# 3. 確保輸出資料夾 outputs/figures 存在
output_fig_dir = os.path.join('outputs', 'figures')
os.makedirs(output_fig_dir, exist_ok=True)

# 設定統一的 matplotlib 畫風
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [8, 6]
plt.rcParams['font.size'] = 12

# ----------------- 圖表一：Group A (CarrotEating & NoSodaDrinking) 比例圖 -----------------
plt.figure()
ax1 = sns.barplot(
    data=df, 
    x='SadOrHopeless', 
    y='Group_A_Diet', 
    errorbar=None, 
    palette='muted'
)

# 更新圖表標題為 NoSodaDrinking
plt.title('Proportion of Group A (Carrot Eating & No Soda Drinking)\nby Mental Well-being Status', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Sad Or Hopeless Status (0 = No, 1 = Yes)', fontsize=12, labelpad=10)
plt.ylabel('Proportion (Success Rate)', fontsize=12, labelpad=10)
plt.xticks([0, 1], ['Not Sad / Hopeless (0)', 'Sad / Hopeless (1)'])
plt.ylim(0, df['Group_A_Diet'].mean() * 2) 

# 在柱狀圖上方加上數值標籤
for p in ax1.patches:
    ax1.annotate(f'{p.get_height():.2%}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='center', 
                 xytext=(0, 8), 
                 textcoords='offset points', 
                 fontweight='bold')

fig1_path = os.path.join(output_fig_dir, 'group_A_diet_proportion.png')
plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"📊 Group A (NoSodaDrinking) 圖表已儲存至: {fig1_path}")


# ----------------- 圖表二：Group B (Behavior) 比例圖 -----------------
plt.figure()
ax2 = sns.barplot(
    data=df, 
    x='SadOrHopeless', 
    y='Group_B_Behavior', 
    errorbar=None, 
    palette='flare'
)

plt.title('Proportion of Group B (Cigarette Use & Sports Participation)\nby Mental Well-being Status', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Sad Or Hopeless Status (0 = No, 1 = Yes)', fontsize=12, labelpad=10)
plt.ylabel('Proportion (Success Rate)', fontsize=12, labelpad=10)
plt.xticks([0, 1], ['Not Sad / Hopeless (0)', 'Sad / Hopeless (1)'])
plt.ylim(0, df['Group_B_Behavior'].mean() * 2) 

for p in ax2.patches:
    ax2.annotate(f'{p.get_height():.2%}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='center', 
                 xytext=(0, 8), 
                 textcoords='offset points', 
                 fontweight='bold')

fig2_path = os.path.join(output_fig_dir, 'group_B_behavior_proportion.png')
plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"📊 Group B 圖表已儲存至: {fig2_path}")

# 3. 計算兩組 (Sad vs Not Sad) 的平均比例作為象限座標
summary = df.groupby('SadOrHopeless')[['Group_A_Diet', 'Group_B_Behavior']].mean().reset_index()

# 提取座標
p0_x = summary.loc[summary['SadOrHopeless'] == 0, 'Group_A_Diet'].values[0]
p0_y = summary.loc[summary['SadOrHopeless'] == 0, 'Group_B_Behavior'].values[0]

p1_x = summary.loc[summary['SadOrHopeless'] == 1, 'Group_A_Diet'].values[0]
p1_y = summary.loc[summary['SadOrHopeless'] == 1, 'Group_B_Behavior'].values[0]

# 4. 開始畫四象限圖
plt.figure(figsize=(9, 8))

# 畫出兩個關鍵群組的點
plt.scatter(p0_x, p0_y, color='#4C72B0', s=300, zorder=5, label='Not Sad / Hopeless (Group 0)')
plt.scatter(p1_x, p1_y, color='#C44E52', s=300, zorder=5, label='Sad / Hopeless (Group 1)')

# 在點旁邊加上標籤與百分比數字
plt.text(p0_x, p0_y + 0.001, f' Not Sad\n (Diet: {p0_x:.2%}, Risk: {p0_y:.2%})', va='bottom', ha='center', fontweight='bold')
plt.text(p1_x, p1_y + 0.001, f' Sad / Hopeless\n (Diet: {p1_x:.2%}, Risk: {p1_y:.2%})', va='bottom', ha='center', fontweight='bold')

# 畫箭頭標示兩組之間的位移軌跡（可以看出心理狀態改變導致的行為位移）
plt.annotate('', xy=(p1_x, p1_y), xytext=(p0_x, p0_y),
             arrowprops=dict(arrowstyle="->", color="gray", lw=2, ls="--"))

# 💡 建立象限黃金交叉線（以兩組的總平均值作為十字交叉線）
mid_x = (p0_x + p1_x) / 2
mid_y = (p0_y + p1_y) / 2
plt.axvline(x=mid_x, color='black', linestyle=':', alpha=0.6)
plt.axhline(y=mid_y, color='black', linestyle=':', alpha=0.6)

# 設定圖表邊界（保留舒適的留白空間）
padding_x = (max(p0_x, p1_x) - min(p0_x, p1_x)) * 0.6
padding_y = (max(p0_y, p1_y) - min(p0_y, p1_y)) * 0.6
plt.xlim(min(p0_x, p1_x) - padding_x, max(p0_x, p1_x) + padding_x)
plt.ylim(min(p0_y, p1_y) - padding_y, max(p0_y, p1_y) + padding_y)

# 加上四個象限的文字標籤（解釋每個角落代表的意思）
plt.text(plt.xlim()[0] + 0.002, plt.ylim()[1] - 0.003, 'Quadrant II\nLow Diet Health\nHigh Risk Behavior', alpha=0.5, fontsize=10, va='top')
plt.text(plt.xlim()[1] - 0.002, plt.ylim()[1] - 0.003, 'Quadrant I\nHigh Diet Health\nHigh Risk Behavior', alpha=0.5, fontsize=10, va='top', ha='right')
plt.text(plt.xlim()[0] + 0.002, plt.ylim()[0] + 0.002, 'Quadrant III\nLow Diet Health\nLow Risk Behavior', alpha=0.5, fontsize=10, va='bottom')
plt.text(plt.xlim()[1] - 0.002, plt.ylim()[0] + 0.002, 'Quadrant IV\nHigh Diet Health\nLow Risk Behavior', alpha=0.5, fontsize=10, va='bottom', ha='right')

# 美化外觀
plt.title('Behavioral Four-Quadrant Matrix Plot\nby Student Mental Well-being Status', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Group A: Carrot Eating & No Soda Drinking (Proportion)', fontsize=12, labelpad=10)
plt.ylabel('Group B: Cigarette Use & Sports Participation (Proportion)', fontsize=12, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(loc='lower left')

# 5. 確保資料夾存在並存檔
output_fig_dir = os.path.join('outputs', 'figures')
os.makedirs(output_fig_dir, exist_ok=True)

fig_path = os.path.join(output_fig_dir, 'behavior_quadrant_matrix.png')
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ EDA 圖表已成功更新並儲存至 outputs/figures 資料夾！")