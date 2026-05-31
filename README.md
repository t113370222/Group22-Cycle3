# 📊 YRBSS 青少年行為與心理健康分析 (Group 16)

---

## 👥 團隊資訊 (Group Information)

* **組別 (Group Number)**: Group 22 / 第 22 組
* **組員名單 (Members)**:
  * `113370217` 黃子芸
  * `111370222` 謝函芸
  
---

## 💾 使用數據 (Dataset)

* **數據集名稱 (Dataset Name)**: 2007 Youth Risk Behavior Surveillance System (YRBSS) / 2007 年青少年危險行為調查
* **來源 (Source)**: Centers for Disease Control and Prevention (CDC) / 美國疾病管制與預防中心

---

## 🔍 選定變數與資料清洗 (Selected Variables & Cleaning)

根據我們的程式碼清洗邏輯，我們將原始 YRBSS 數據重碼並合併為以下核心變數：

### 1. 心理健康狀態 (`SadOrHopeless`)
* **`1`**: 過去一年曾連續兩週以上感到傷心或絕望（原編碼 `1` 轉為 `1`）
* **`0`**: 未感到傷心或絕望（原編碼 `2` 轉為 `0`）

### 2. 飲食習慣組合 (`GroupA_Diet_Healthy`)
* **`1`**: 滿足健康飲食組合（有吃胡蘿蔔 `CarrotEating == 1` **且** 不喝汽水 `NoSodaDrinking == 1`）
* **`0`**: 其他飲食組合（未吃胡蘿蔔或有喝汽水）

### 3. 風險代償行為 (`GroupB_Risk_Behavior`)
* **`1`**: 滿足風險代償組合（有吸菸 `CurrentCigaretteUse == 1` **且** 有參與運動隊伍 `SportsTeamParticipation == 1`）
* **`0`**: 其他行為組合

---

## 📍 基準值設定 (Benchmark Values)

我們根據「行為四象限矩陣圖」中，代表交叉基準線的灰色虛線切點設定基準率：

| 評估項目 (Items) | 變數代號 | 基準率 (Benchmark Value) |
| :--- | :--- | :--- |
| **飲食習慣組合基準率** | $p_{A0}$ | **0.084 (8.4%)** |
| **風險代償行為基準率** | $p_{B0}$ | **0.091 (9.1%)** |

---

## ❓ 研究問題 (Project Questions)

### 📌 1. 健康飲食比例推論 (Proportion Inference - Group A)
* **English:** Is the proportion of students maintaining healthy dietary habits (Carrot Eating & No Soda Drinking) significantly different between those who felt sad/hopeless and those who did not?
* **中文:** 學生維持健康飲食（有吃胡蘿蔔且不喝汽水）的比例，在「傷心/絕望」與「不傷心」的群體之間是否具有顯著差異？

### 📌 2. 風險代償行為比例推論 (Proportion Inference - Group B)
* **English:** Is the proportion of students exhibiting risk-compensatory behaviors (Cigarette Use & Sports Participation) significantly different between those who felt sad/hopeless and those who did not?
* **中文:** 學生展現風險代償行為（同時有吸菸與參與運動隊伍）的比例，在「傷心/絕望」與「不傷心」的群體之間是否具有顯著差異？
