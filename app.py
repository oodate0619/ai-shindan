import streamlit as st
import pandas as pd
import plotly.express as px

# ページ基本設定（タイトルやアイコン）
st.set_page_config(page_title="AI業務改善診断", layout="centered")

# カスタムCSSでスマホでの見栄えを調整
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 生成AI導入・業務改善診断")
st.write("5つの質問に答えるだけで、AIによる削減時間と投資対効果を算出します。")

# --- 質問フォーム ---
with st.form("diagnostic_form"):
    st.subheader("📋 ヒアリング項目")
    
    industry = st.selectbox("Q1. 業種を選択してください", 
                            ["ICT・情報通信", "専門サービス（コンサル・士業）", "小売・EC", "製造・建設", "運輸・物流", "医療・福祉", "その他"])
    
    staff_count = st.number_input("Q2. 導入対象の従業員数（名）", min_value=1, value=5)
    
    hours_per_week = st.slider("Q3. 1人あたり週に何時間『書類作成・メール・調査』をしていますか？", 0, 40, 10)
    
    pain_point = st.radio("Q4. 一番解決したい課題は何ですか？",
                         ["人手不足・採用難", "事務作業による残業", "属人化・社長の多忙", "売上を作る時間の不足"])
    
    barrier = st.selectbox("Q5. AI導入の最大の不安は？",
                          ["使いこなせるか不安", "セキュリティ・情報漏洩", "心理的抵抗・面倒くさい", "費用対効果が見えない"])
    
    # 診断実行ボタン
    submitted = st.form_submit_button("✨ 診断レポートを生成する")

# --- 診断ロジック（ボタンが押された後のみ実行） ---
if submitted:
    # 業種別係数
    industry_factor = {"ICT・情報通信": 1.2, "専門サービス（コンサル・士業）": 1.1, "小売・EC": 1.0, "製造・建設": 0.8, "運輸・物流": 0.7, "医療・福祉": 0.6, "その他": 0.9}
    w = industry_factor.get(industry, 1.0)

    # 削減時間（効率化率50%と想定）
    saved_hours_monthly = (hours_per_week * 4 * staff_count) * 0.5 * w
    # 創出価値（時給2,500円換算）
    monthly_value = saved_hours_monthly * 2500

    # スクロールで見やすい位置へ
    st.write("---")
    st.header("📊 診断結果レポート")
    
    # 指標を大きな数字で表示
    col1, col2 = st.columns(2)
    col1.metric("月間創出可能時間", f"{int(saved_hours_monthly)} 時間")
    col2.metric("年間期待付加価値", f"¥{int(monthly_value * 12):,}")

    # ROIグラフ
    st.subheader("📈 導入後のインパクト（月額）")
    df = pd.DataFrame({
        "状態": ["現状のコスト", "AI導入後の価値"],
        "金額": [(hours_per_week * 4 * staff_count * 2500), monthly_value]
    })
    fig = px.bar(df, x="状態", y="金額", color="状態", text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)

    # 具体的なアドバイス
    st.success(f"### 💡 戦略アドバイス\n"
               f"貴社の業種（{industry}）はAI適性が非常に高いです。\n"
               f"まずは「{pain_point}」を解消するため、日常のルーチン作業をAIに丸投げする環境を整えましょう。")

    # 90日ロードマップ
    st.subheader("🗓 導入定着までの90日")
    roadmap = pd.DataFrame({
        "期間": ["30日", "60日", "90日"],
        "目標": ["嫌な仕事の代行", "標準テンプレ化", "自走体制構築"]
    })
    st.table(roadmap)

    # お問い合わせ導線
    st.write("---")
    st.markdown("### 📞 より詳細な診断・導入相談はこちら")
    st.link_button("無料相談を予約する（Googleフォーム等）", "https://forms.gle/your-form-url")
