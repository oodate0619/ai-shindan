import streamlit as st
import pandas as pd
import plotly.express as px

# ページ基本設定
st.set_page_config(page_title="AI業務改善診断", layout="centered")

# カスタムCSSでスマホ対応とデザイン調整
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        border: none;
    }
    /* LINEボタン専用のデザイン */
    .line-button {
        display: inline-block;
        width: 100%;
        text-align: center;
        background-color: #06C755;
        color: white;
        padding: 15px;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 生成AI導入・業務改善診断")
st.write("わずか5つの質問で、あなたの会社の『AIによる伸びしろ』を可視化します。")

# --- 質問フォーム ---
with st.form("diagnostic_form"):
    st.subheader("📋 現状のヒアリング")
    
    industry = st.selectbox("Q1. 業種を選択してください", 
                            ["ICT・情報通信", "専門サービス（コンサル・士業）", "小売・EC", "製造・建設", "運輸・物流", "医療・福祉", "その他"])
    
    staff_count = st.number_input("Q2. 導入対象の従業員数（名）", min_value=1, value=5)
    
    hours_per_week = st.slider("Q3. 1人あたり週に何時間『書類作成・メール・調査』をしていますか？", 0, 40, 10)
    
    pain_point = st.radio("Q4. 一番解決したい課題は何ですか？",
                         ["人手不足・採用難", "事務作業による残業", "属人化・社長の多忙", "売上を作る時間の不足"])
    
    barrier = st.selectbox("Q5. AI導入の最大の不安は？",
                          ["使いこなせるか不安", "セキュリティ・情報漏洩", "心理的抵抗・面倒くさい", "費用対効果が見えない"])
    
    submitted = st.form_submit_button("✨ 診断結果を表示する")

# --- 診断ロジック ---
if submitted:
    # 業種別係数（実証データに基づく重み付け） [cite: 4, 12]
    industry_factor = {"ICT・情報通信": 1.2, "専門サービス（コンサル・士業）": 1.1, "小売・EC": 1.0, "製造・建設": 0.8, "運輸・物流": 0.7, "医療・福祉": 0.6, "その他": 0.9}
    w = industry_factor.get(industry, 1.0)

    # 削減時間の算出（初期定着フェーズの期待効率化率50%と設定） [cite: 9, 24]
    saved_hours_monthly = (hours_per_week * 4 * staff_count) * 0.5 * w
    # 創出価値（付加価値単価2,500円換算）
    monthly_value = saved_hours_monthly * 2500

    st.write("---")
    st.header("📊 診断レポート")
    
    col1, col2 = st.columns(2)
    col1.metric("月間創出可能時間", f"{int(saved_hours_monthly)} 時間")
    col2.metric("年間期待付加価値", f"¥{int(monthly_value * 12):,}")

    # ROIグラフ
    st.subheader("📈 導入によるインパクト予測（月額）")
    df = pd.DataFrame({
        "状態": ["現状の事務コスト", "AI導入による改善効果"],
        "価値": [(hours_per_week * 4 * staff_count * 2500), monthly_value]
    })
    fig = px.bar(df, x="状態", y="価値", color="状態", text_auto='.2s', color_discrete_sequence=['#CBD5E0', '#007bff'])
    st.plotly_chart(fig, use_container_width=True)

    # 戦略アドバイス（トーン修正版）
    st.success(f"### 💡 戦略アドバイス\n"
               f"貴社の業種（{industry}）と「{pain_point}」という課題に対して、生成AIは非常に強力な代替労働力となります。\n\n"
               f"まずは、最も心理的負荷が高い『嫌なルーチン業務』から順次AIへ移行することで、**現場の負担を劇的に減らしつつ、本来取り組むべき業務に集中できる環境を整えることができます。**")

    # ロードマップ（N段階モデルに基づく設計） [cite: 11, 21]
    st.subheader("🗓 導入・定着へのステップ")
    roadmap_data = {
        "期間": ["1ヶ月目（N1）", "2ヶ月目（N2-3）", "3ヶ月目（N4）"],
        "目標": ["成功体験の獲得", "業務の標準化", "自走体制の確立"],
        "内容": ["嫌な作業のAI代行", "部門別テンプレ整備", "教育フロー構築"]
    }
    st.table(pd.DataFrame(roadmap_data))

    # LINE導線
    st.write("---")
    st.subheader("✅ まずは気軽に無料でご相談ください")
    st.write("具体的な活用方法や、自社に合わせたカスタマイズについて、大館が直接お答えします。")
    
    st.markdown('<a href="https://line.me/ti/p/zUSQ7mCx7F" class="line-button">💬 大館のLINEでお気軽にご質問ください</a>', unsafe_allow_html=True)
