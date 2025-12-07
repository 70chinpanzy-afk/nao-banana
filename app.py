import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import time
import base64

# ページ設定
st.set_page_config(
    page_title="Enjoy Banana - 画像生成",
    page_icon="🍌",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 0.75rem;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        border-radius: 4px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# サイドバー設定
with st.sidebar:
    st.title("⚙️ 設定")
    
    # APIキー入力
    api_key = st.text_input(
        "Google API キー",
        type="password",
        help="Google AI Studio (https://aistudio.google.com/app/apikey) で取得できます"
    )
    
    # セキュリティに関する情報
    st.markdown("""
    <div class="info-box">
        🔒 <strong>プライバシー保護</strong><br>
        APIキーはブラウザにのみ保存され、サーバーには送信されません。
        セッション終了時に自動的に削除されます。
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # モデル情報
    st.subheader("📊 使用モデル")
    st.info("**Gemini 3 Pro Image**\n\n最新のAI画像生成モデルで、誰でも手軽に高品質な画像を作成できます！")
    
    st.divider()
    
    # 使い方
    with st.expander("📖 使い方"):
        st.markdown("""
        1. Google API キーを入力
        2. 生成したい画像の説明を入力
        3. 「画像を生成する」ボタンをクリック
        4. 生成された画像が表示されます
        
        **ヒント:**
        - 詳細な説明ほど良い結果が得られます
        - 英語でも日本語でも使用可能です
        """)

# メイン画面
st.title("🍌 Enjoy Banana")
st.subheader("誰でも簡単にAI画像生成を楽しめるツール")

# APIキーチェック
if not api_key:
    st.warning("⚠️ サイドバーからGoogle API キーを入力してください。")
    st.info("API キーは [Google AI Studio](https://aistudio.google.com/app/apikey) で無料で取得できます。")
    st.stop()

# プロンプト入力エリア
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area(
        "画像の説明を入力してください",
        height=150,
        placeholder="例: 夕暮れの海辺で遊ぶ子猫、水彩画風、温かい色調",
        help="生成したい画像を詳しく説明してください"
    )

with col2:
    st.markdown("### 💡 プロンプト例")
    example_prompts = [
        "未来都市の夜景、ネオンライト",
        "森の中の小さな家、ファンタジー風",
        "宇宙飛行士が月面を歩く、リアル",
        "カラフルな花畑、油絵風"
    ]
    
    for example in example_prompts:
        if st.button(example, key=example, use_container_width=True):
            prompt = example
            st.rerun()

# 生成ボタン
generate_button = st.button("🎨 画像を生成する", type="primary", use_container_width=True)

# 画像生成処理
if generate_button:
    if not prompt.strip():
        st.error("❌ プロンプトを入力してください。")
    else:
        try:
            # APIキーを設定してクライアントを初期化
            client = genai.Client(api_key=api_key)
            
            # プログレスバー表示
            with st.spinner("🎨 画像を生成中..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # モデル初期化
                status_text.text("Gemini 3 Pro Image モデルを初期化中...")
                progress_bar.progress(25)
                
                # 画像生成リクエスト
                status_text.text("画像を生成中... (30秒ほどかかる場合があります)")
                progress_bar.progress(50)
                
                # Gemini 3 Pro Image を使用して画像生成
                response = client.models.generate_content(
                    model='gemini-3-pro-image-preview',
                    contents=prompt
                )
                
                progress_bar.progress(75)
                status_text.text("画像を処理中...")
                
                # レスポンスから画像を取得
                image_found = False
                if response.candidates and len(response.candidates) > 0:
                    for part in response.candidates[0].content.parts:
                        # 画像データを探す
                        if hasattr(part, 'inline_data') and part.inline_data:
                            # 画像データを取得
                            image_data = part.inline_data.data
                            mime_type = part.inline_data.mime_type
                            
                            # PIL Imageに変換
                            pil_image = Image.open(io.BytesIO(image_data))
                            
                            # 画像を表示
                            progress_bar.progress(100)
                            status_text.empty()
                            progress_bar.empty()
                            
                            st.success("✅ 画像の生成が完了しました！")
                            
                            # 画像を表示
                            st.image(pil_image, caption=f"生成されたプロンプト: {prompt}", use_container_width=True)
                            
                            # ダウンロードボタン
                            st.download_button(
                                label="📥 画像をダウンロード",
                                data=image_data,
                                file_name=f"enjoy_banana_{int(time.time())}.png",
                                mime=mime_type,
                                use_container_width=True
                            )
                            
                            image_found = True
                            break
                
                if not image_found:
                    progress_bar.empty()
                    status_text.empty()
                    st.error("❌ 画像の生成に失敗しました。")
                    if response.text:
                        st.info(f"レスポンス: {response.text}")
                    
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            
            # エラーの種類に応じたヘルプメッセージ
            error_message = str(e).lower()
            
            if "api key" in error_message or "authentication" in error_message:
                st.markdown("""
                <div class="error-message">
                    <strong>APIキーエラー</strong><br>
                    APIキーが無効です。以下を確認してください：<br>
                    • APIキーが正しく入力されているか<br>
                    • APIキーが有効化されているか<br>
                    • Generative AI APIが有効になっているか
                </div>
                """, unsafe_allow_html=True)
            elif "quota" in error_message or "limit" in error_message:
                st.markdown("""
                <div class="error-message">
                    <strong>クォータエラー</strong><br>
                    APIの使用制限に達しました。しばらく待ってから再度お試しください。
                </div>
                """, unsafe_allow_html=True)
            elif "safety" in error_message or "blocked" in error_message:
                st.markdown("""
                <div class="error-message">
                    <strong>安全性フィルター</strong><br>
                    プロンプトが安全性フィルターによってブロックされました。<br>
                    別の表現でお試しください。
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("詳細なエラー情報を確認し、プロンプトを変更するか、しばらく待ってから再度お試しください。")

# フッター
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Made with ❤️ using Streamlit and Google Generative AI
</div>
""", unsafe_allow_html=True)
