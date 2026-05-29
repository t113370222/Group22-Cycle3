import pandas as pd
import os

# 1. 取得這份程式碼目前的絕對路徑
current_path = os.path.abspath(os.getcwd())
output_dir = os.path.join(current_path,  'data', 'processed')

# 2. 強制建立多層資料夾
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"--- 步驟 1: 資料夾確認 ---")
    print(f"目標資料夾已準備好：{output_dir}")
except Exception as e:
    print(f"建立資料夾失敗，錯誤原因: {e}")
# 3. 讀取資料集
# 請確保 YRBS_2007.csv 檔案在您的程式執行目錄下
df = pd.read_csv('data/raw/YRBS_2007.csv')

# 4. 依照指令轉換數據
# SadOrHopeless: success (1) -> 1, failure (2) -> 0
df['SadOrHopeless'] = df['SadOrHopeless'].map({1: 1, 2: 0})

# CurrentCigaretteUse: success (2-7) -> 1, failure (1) -> 0
def process_cigarette(val):
    if val == 1:
        return 0
    elif 2 <= val <= 7:
        return 1
    else:
        return None # 處理缺失或異常值

df['CurrentCigaretteUse'] = df['CurrentCigaretteUse'].apply(process_cigarette)


# SportsTeamParticipation: success (2-4) -> 1, failure (1) -> 0
def process_sportsteam(val):
    if val == 1:
        return 0
    elif 2 <= val <= 4:
        return 1
    else:
        return None # 處理缺失或異常值

df['SportsTeamParticipation'] = df['SportsTeamParticipation'].apply(process_sportsteam)

def process_carroteating(val):
    if val == 1:
        return 0
    elif 2 <= val <= 7:
        return 1
    else:
        return None # 處理缺失或異常值

df['CarrotEating'] = df['CarrotEating'].apply(process_carroteating)

def process_NoSodaDrinking(val):
    if val == 1:
        return 0
    elif 2 <= val <= 7:
        return 1
    else:
        return None # 處理缺失或異常值

df['NoSodaDrinking'] = df['NoSodaDrinking'].apply(process_NoSodaDrinking)

# 5. 儲存至指定路徑
output_path = os.path.join(output_dir, 'YRBS_2007_cleaned.csv')
df.to_csv(output_path, index=False)

print(f"成功！檔案已儲存至：{output_path}")