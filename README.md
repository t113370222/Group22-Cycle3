# 📊 YRBSS 青少年行為與心理健康分析 / Adolescent Behavior & Mental Well-being Analysis (Group 22)

---

## 👥 團隊資訊 / Group Information

* **組別 / Group Number**: Group 22 / 第 22 組
* **組員名單 / Members**:
  * `113370217` 黃子芸
  * `113370222` 謝函芸
---

## 💾 使用數據 / Dataset

* **數據集名稱 / Dataset Name**: 
  * 2007 Youth Risk Behavior Surveillance System (YRBSS)
  * 2007 年青少年危險行為調查
* **來源 / Source**: 
  * Centers for Disease Control and Prevention (CDC)
  * 美國疾病管制與預防中心

---

## 🔍 選定變數與資料清洗 / Selected Variables & Data Cleaning

根據我們的 Python 程式碼，我們將原始 YRBSS 數據重碼，並依據雙重條件合成核心複分類變數：
According to our Python data cleaning logic, the original YRBSS variables are recoded and combined into core joint behavioral indicators:

### 1. 心理健康狀態 / Mental Well-being Status (`SadOrHopeless`)
* **`1` (Success)**: 過去一年曾連續兩週以上感到傷心或絕望 / Felt sad or hopeless for $\ge$ 2 weeks in a row.
* **`0` (Failure)**: 未感到傷心或絕望 / Did not feel sad or hopeless.

### 2. 飲食習慣組合 / Dietary Habit Combination (`Group_A_Diet`)
* **`1` (Success)**: 滿足健康飲食組合（有吃胡蘿蔔 `CarrotEating == 1` **且** 不喝汽水 `NoSodaDrinking == 1`）/ Eating carrots AND No soda drinking.
* **`0` (Failure)**: 其他飲食組合（未吃胡蘿蔔或有喝汽水）/ Other dietary combinations.

### 3. 風險代償行為 / Risk-Compensatory Behavior (`Group_B_Behavior`)
* **`1` (Success)**: 滿足風險代償組合（有吸菸 `CurrentCigaretteUse == 1` **且** 有參與運動隊伍 `SportsTeamParticipation == 1`）/ Current cigarette use AND Active sports team participation.
* **`0` (Failure)**: 其他行為組合 / Other behavioral combinations.

---

## 📊 統計檢定方法 / Statistical Methodology

我們採用 **雙母體比例差異 Z 檢定 (Two-Proportion Z-Test)** 進行統計推論，比較不同心理狀態群體下的行為比例差異，並計算 95% 差異信賴區間。
We applied the **Two-Proportion Z-Test** for statistical inference to evaluate behavioral proportion differences between distinct mental states, along with 95% Confidence Intervals (CI).

---

## ❓ 研究問題 / Project Questions

### 📌 1. 健康飲食比例差異檢定 / Two-Proportion Z-Test (Group A)
* **English:** Is the proportion of students maintaining healthy dietary habits (`Group_A_Diet`) significantly different between students who felt sad/hopeless ($p_1$) and those who did not ($p_0$)? 
* **中文:** 學生維持健康飲食習慣（`Group_A_Diet`）的比例，在「傷心/絕望（$p_1$）」與「不傷心（$p_0$）」兩個獨立群體之間是否具有統計學上的顯著差異？

* **Hypothesis:** $H_0: p_1 = p_0$ vs $H_1: p_1 \neq p_0$

### 📌 2. 風險代償行為比例差異檢定 / Two-Proportion Z-Test (Group B)
* **English:** Is the proportion of students exhibiting risk-compensatory behaviors (`Group_B_Behavior`) significantly different between students who felt sad/hopeless ($p_1$) and those who did not ($p_0$)?
* **中文:** 學生展現風險代償行為（`Group_B_Behavior`）的比例，在「傷心/絕望（$p_1$）」與「不傷心（$p_0$）」兩個獨立群體之間是否具有統計學上的顯著差異？
* **Hypothesis:** $H_0: p_1 = p_0$ vs $H_1: p_1 \neq p_0$

---
## 🎥Presentation Video link
https://drive.google.com/file/d/1C__ZIcVm8aRm_ezh8IG6e_Wt-qGKpG6r/view?usp=drive_link
