import streamlit as st
import pandas as pd
import plotly.express as px

# ページ基本設定
st.set_page_config(page_title="AI業務改善診断", layout="centered")

# カスタムCSS（スマホ最適化・LINEボタン・特典枠）
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
    .bonus-box {
        background-color: #fff9db; padding: 20px; border-radius: 12px;
        border: 2px dashed #fcc419; margin-top: 20px;
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

    # 業種別アドバイス & プロンプト特典
    content_map = {
        "ICT・情報通信": {
            "advice": "ドキュメント作成や要約が業務の核となるため、提案書骨子や議事録のToDo化を自動化することで、本来の付加価値業務に集中できる環境を整えることができます [cite: 12, 43]。",
            "prompt": "【議事録を瞬時にToDoリスト化】\n「以下の会議の書き起こしから、1.決定事項、2.誰が、3.いつまでに、4.何をすべきか、を箇条書きで抽出してください。 [会議の内容をここに貼る]」"
        },
        "専門サービス（コンサル・士業）": {
            "advice": "法令調査や定型メールの作成をAIに任せることで、専門家としての高度な判断や顧客対応に時間を割ける環境を整えることができます [cite: 13, 87]。",
            "prompt": "【難しい相談への一次回答案】\n「あなたは経験豊富な専門家です。以下の顧客からの相談に対し、安心感を与えつつ、必要な確認事項を3点に絞った丁寧な返信案を作成してください。 [相談内容をここに貼る]」"
        },
        "小売・EC": {
            "advice": "商品説明文の量産やSNS投稿案をAIで回すことで、少人数でも質の高い販促活動を継続できる環境を整えることができます [cite: 5, 15]。",
            "prompt": "【売れる商品説明への変換】\n「以下の商品の『特徴』を、ターゲット顧客の『メリット』に変換した魅力的なキャッチコピーと説明文を作成してください。 [商品の特徴をここに貼る]」"
        },
        "製造・建設": {
            "advice": "現場での音声入力を活用した日報作成やノウハウの形式知化により、二度手間を解消し、教育コストを大幅に下げる環境を整えることができます [cite: 18, 186, 219]。",
            "prompt": "【音声メモから完璧な日報作成】\n「以下の箇条書き（または音声入力テキスト）をもとに、5W1Hが整理された報告書形式に整えてください。 [現場のメモをここに貼る]」"
        },
        "運輸・物流": {
            "advice": "点呼簿のデジタル化や値上げ交渉等の心理的負荷が高いメール作成をAIで補助することで、管理者の負担を激減させる環境を整えることができます [cite: 266, 267]。",
            "prompt": "【角が立たない価格改定のお願い】\n「燃料費高騰に伴う運送料金改定のお願いを、長年の取引への感謝を込めつつ、誠実で納得感のある文章で作成してください。 [現在の状況をここに貼る]」"
        },
        "医療・福祉": {
            "advice": "記述義務があるケアプラン等の叩き台をAIが支援することで、記録作業の時間を削減し、本来のケアに注力できる環境を整えることができます [cite: 19, 266]。",
            "prompt": "【個人情報を伏せたケア記録の要約】\n「以下のケア中の観察メモから、特記事項を抽出し、専門的な報告書形式の叩き台を作成してください（※氏名等の個人情報は伏せています）。 [観察メモをここに貼る]」"
        }
    }
    target_content = content_map.get(industry, {"advice": "AIを『代替労働力』と定義し、事務作業の0→1を任せることで生産性を劇的に向上させる環境を整えることができます [cite: 266, 273]。", "prompt": "【日常業務の時短】\n「以下の業務の要点を、3つのステップで実行できるToDoリストに変換してください。 [業務内容をここに貼る]」"})

    # 数値算出（CSOロジック）
    # 月間創出価値 $V_{profit}$ の算出
    saved_hours_monthly = (hours_per_week * 4 * staff_count) * 0.5 * w
    monthly_value = saved_hours_monthly * 2500

    st.write("---")
    st.header("📊 診断レポート")
    col1, col2 = st.columns(2)
    col1.metric("月間創出可能時間", f"{int(saved_hours_monthly)} 時間")
    col2.metric("年間期待付加価値", f"¥{int(monthly_value * 12):,}")

    # ROIグラフ
    st.subheader("📈 インパクト予測（月額）")
    df = pd.DataFrame({"状態": ["現状コスト", "改善効果"], "価値": [(hours_per_week * 4 * staff_count * 2500), monthly_value]})
    fig = px.bar(df, x="状態", y="価値", color="状態", text_auto='.2s', color_discrete_sequence=['#CBD5E0', '#007bff'])
    st.plotly_chart(fig, use_container_width=True)

    # アドバイス
    st.success(f"### 💡 {industry}特化アドバイス\n{target_content['advice']}")

    # 🎁 特典セクション
    st.markdown(f"""
        <div class="bonus-box">
            <h3 style="margin-top:0;">🎁 特典：明日から使える『魔法のプロンプト』</h3>
            <p>このままChatGPT等にコピー＆ペーストして使えます：</p>
            <div style="background-color: white; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; font-family: monospace;">
                {target_content['prompt'].replace('\n', '<br>')}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ロードマップ
    st.subheader("🗓 導入ステップ")
    st.table(pd.DataFrame({"期間": ["1ヶ月目（N1）", "2ヶ月目（N2-3）", "3ヶ月目（N4）"], "目標": ["成功体験", "標準化", "自走体制"], "内容": ["嫌な作業の代替", "テンプレ整備", "教育フロー構築"]}))

    # LINE導線
    st.write("---")
    st.subheader("✅ まずは気軽に無料でご相談ください")
    st.write("このプロンプトの使いこなし方や、貴社専用のカスタマイズについて大館がお答えします。")
    st.markdown('<a href="https://line.me/ti/p/zUSQ7mCx7F" class="line-button">💬 大館のLINEでお気軽にご質問ください</a>', unsafe_allow_html=True)
