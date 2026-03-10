import streamlit as st
import pandas as pd
import plotly.express as px

# ページ基本設定
st.set_page_config(page_title="AI業務改善診断", layout="centered")

# カスタムCSS（スマホ・LINE導線最適化）
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background-color: #007bff; color: white; font-weight: bold; font-size: 1.1em; border: none;
    }
    .line-button {
        display: inline-block; width: 100%; text-align: center;
        background-color: #06C755; color: white; padding: 15px;
        text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 生成AI導入・業務改善診断")
st.write("業界特有の課題に基づき、あなたの会社の『AIによる伸びしろ』を可視化します。")

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
    # 業種別係数
    industry_factor = {"ICT・情報通信": 1.2, "専門サービス（コンサル・士業）": 1.1, "小売・EC": 1.0, "製造・建設": 0.8, "運輸・物流": 0.7, "医療・福祉": 0.6, "その他": 0.9}
    w = industry_factor.get(industry, 1.0)

    # 業種別・悩み別のアドバイス辞書（CSO戦略に基づく）
    advice_dict = {
        "ICT・情報通信": "ドキュメント作成や要約が業務の核となるため、提案書骨子や議事録のToDo化を自動化することで、エンジニアが開発に没頭できる環境を整えることができます。",
        "専門サービス（コンサル・士業）": "過去の事例や法令の調査、定型メールの作成をAIに任せることで、専門家としての高度な判断や顧客対応に時間を割ける環境を整えることができます。",
        "小売・EC": "商品説明文の量産や、SNS投稿案、FAQ対応の自動化により、少人数でも質の高い販促活動を24時間体制で回せる環境を整えることができます。",
        "製造・建設": "現場での音声入力を活用した日報作成や、ベテランのノウハウの形式知化を進めることで、若手の教育コストを下げ、現場の二度手間を解消する環境を整えることができます。",
        "運輸・物流": "点呼簿や配車表のデジタル化、複雑な値上げ交渉メールの文案作成をAIで補助することで、管理者の精神的負荷を減らし、業務を標準化する環境を整えることができます。",
        "医療・福祉": "膨大な記述義務があるケアプランや申し送りの叩き台作成をAIが支援することで、記録作業の時間を削減し、本来のケア業務に注力できる環境を整えることができます。",
        "その他": "日常のメール、調査、資料作成の『初稿（0→1）』をAIに任せ、人は『確認・修正（1→10）』に特化することで、生産性を劇的に向上させる環境を整えることができます。"
    }

    saved_hours_monthly = (hours_per_week * 4 * staff_count) * 0.5 * w
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

    # パーソナライズされた戦略アドバイス
    st.success(f"### 💡 {industry}特化のアドバイス\n"
               f"{industry}において「{pain_point}」を解消するには、AIを単なるツールではなく『代替労働力』と定義することが不可欠です。\n\n"
               f"{advice_dict.get(industry, advice_dict['その他'])}")

    # ロードマップ
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
