import streamlit as st
import pandas as pd
import plotly.express as px

# --- アプリ設定 ---
st.set_page_config(page_title="中小企業AI改善診断", layout="wide")
st.title("🚀 生成AI導入・業務改善診断（CSO Edition）")
st.write("---")

# --- 1. 質問セクション（サイドバーまたはメイン） ---
with st.sidebar:
    st.header("📋 企業ヒアリング")
    industry = st.selectbox("Q1. 業種を選択してください", 
                            ["ICT・情報通信", "専門サービス（士業・コンサル）", "小売・EC", "建設・不動産", "運輸・製造", "医療・福祉"])
    
    pain_task = st.selectbox("Q2. 最も『苦痛』な業務は？",
                             ["顧客への提案・お詫びメール", "日報・現場報告書", "市場調査・ナレッジ検索", "求人票・社内規定作成"])
    
    barrier = st.radio("Q3. 導入にあたっての最大の懸念は？",
                        ["社員の心理的抵抗・不安", "使い方がわからない", "セキュリティ・情報漏洩", "経営層の承認が下りない"])
    
    target = st.radio("Q4. どちらの状態を目指しますか？",
                       ["社長の分身（右腕）を増やしたい", "現場の事務処理能力を底上げしたい"])
    
    staff_count = st.number_input("Q5. 対象となる従業員数（名）", min_value=1, value=5)
    hours_per_week = st.slider("対象業務に費やしている週あたりの時間（人/時間）", 1, 20, 5)

# --- 2. 診断ロジック（CSO判定エンジン） ---
# 業種別重み（W_industry）
industry_weights = {
    "ICT・情報通信": 1.2, "専門サービス（士業・コンサル）": 1.1, "小売・EC": 1.0,
    "建設・不動産": 0.8, "運輸・製造": 0.7, "医療・福祉": 0.6
}
w_ind = industry_weights.get(industry, 1.0)

# 改善率（E_ratio）
e_ratio = 0.5 # 初期定着フェーズでの期待改善率（50%）

# 創出価値（Value Calculation）
# 付加価値単価を2,500円（人件費2,000円 + 期待利益500円）と定義
monthly_hours_saved = (hours_per_week * 4 * staff_count) * w_ind * e_ratio
monthly_value_creation = monthly_hours_saved * 2500

# 分岐判定
branch = "A：社長の右腕化" if target == "社長の分身（右腕）を増やしたい" else "B：社員の戦力化"

# T型障壁判定
t_type = {"社員の心理的抵抗・不安": "T1（心理抵抗）", 
          "使い方がわからない": "T2（方法不明）",
          "セキュリティ・情報漏洩": "T3（ルールの壁）",
          "経営層の承認が下りない": "T4（承認停滞）"}.get(barrier)

# --- 3. 結果表示セクション ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 診断結果レポート")
    st.subheader(f"戦略方針：{branch}")
    st.write(f"あなたの企業のAI活用ポテンシャルは **{int(w_ind * 80)}点** です。")
    
    # 指標のハイライト
    st.metric("月間創出可能時間", f"{int(monthly_hours_saved)} 時間")
    st.metric("年間期待付加価値", f"¥{int(monthly_value_creation * 12):,}")

    st.info(f"💡 **CSOの処方箋：** 貴社は現在 **{t_type}** の状態です。まずは『{pain_task}』からAIに代替させ、成功体験（N1）を作りましょう。")

with col2:
    st.header("🚀 3ヶ月のロードマップ")
    st.write("1. **30日目**: 『嫌な仕事』のAI代行開始（N1）")
    st.write("2. **60日目**: 部門別テンプレ化・型化（N3）")
    st.write("3. **90日目**: 自走体制・教育フロー構築（N4）")

# --- 4. グラフ表示 ---
st.write("---")
st.subheader("業種別・タスク別の改善期待値")
df_viz = pd.DataFrame({
    "カテゴリー": ["現状の業務コスト", "AI導入後の改善余地"],
    "価値（月換算）": [hours_per_week * 4 * staff_count * 2500, monthly_value_creation]
})
fig = px.bar(df_viz, x="カテゴリー", y="価値（月換算）", color="カテゴリー", text_auto=True)
st.plotly_chart(fig, use_container_width=True)
