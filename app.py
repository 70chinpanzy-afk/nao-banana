import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import time

# ページ設定
st.set_page_config(
    layout="wide",
    page_title="Enjoy Banana Ver 3.0",
    page_icon="🍌",
    initial_sidebar_state="collapsed"
)

# セッション状態の初期化
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# カスタムCSS - プロフェッショナルでモダンなデザイン
st.markdown("""
<style>
    /* メイン背景 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* ヘッダースタイル */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 400;
    }
    
    /* カードスタイル */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* プレビューエリア */
    .preview-area {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* フッター */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    /* テキストエリアのスタイル */
    .stTextArea textarea {
        font-size: 16px;
        border-radius: 12px;
    }
    
    /* ボタンのスタイル */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
    }
    
    /* インフォボックス */
    .info-box {
        background: #e7f3ff;
        border-left: 4px solid #2196F3;
        color: #12324a;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        color: #10351d;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #4a3800;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="header-container">
    <div class="header-title">🍌 Enjoy Banana Ver 3.0</div>
    <div class="header-subtitle">誰でも簡単にAI画像生成を楽しめるプロフェッショナルツール - 画風選択機能搭載</div>
</div>
""", unsafe_allow_html=True)

# 2カラムレイアウト
col_left, col_right = st.columns([1, 1], gap="large")

# 左カラム: 設定・プロンプト入力エリア
with col_left:
    # APIキー入力カード
    st.markdown("### 🔑 API設定")
    
    api_key = st.text_input(
        "Google API キー",
        type="password",
        placeholder="APIキーを入力してください",
        help="Google AI Studio (https://aistudio.google.com/app/apikey) で取得できます"
    )
    
    if api_key:
        st.markdown('<div class="success-box">✅ APIキーが設定されました</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ APIキーを入力してください</div>', unsafe_allow_html=True)
    
    with st.expander("🔒 プライバシーについて"):
        st.markdown("""
        - APIキーはこのアプリによってファイル保存されません
        - Streamlitの実行プロセスからGoogle Gemini APIの呼び出しに使用されます
        - 共有サーバーで公開する場合は、事前に認証と秘密情報の扱いを確認してください
        """)
    st.divider()
    
    # プロンプト入力カード
    st.markdown("### ✨ 画像生成")
    
    # スタイル選択ドロップダウン
    style = st.selectbox(
        "🎨 画風を選択（オプション）",
        ["指定なし", "アニメ風イラスト", "リアルな写真", "3Dレンダリング", "ドット絵", "水彩画風", "サイバーパンク"],
        help="画風を選択すると、プロンプトに自動的に追加されます"
    )
    
    prompt = st.text_area(
        "生成したい画像の説明を入力",
        height=150,
        placeholder="例: 夕暮れの海辺で遊ぶ子猫",
        help="詳細に説明するほど、より良い結果が得られます"
    )
    
    # プロンプト例
    st.markdown("**💡 プロンプト例**")
    example_col1, example_col2 = st.columns(2)
    
    example_prompts = [
        "未来都市の夜景、ネオンライト",
        "森の中の小さな家、ファンタジー風",
        "宇宙飛行士が月面を歩く、リアル",
        "カラフルな花畑、油絵風"
    ]
    
    for i, example in enumerate(example_prompts):
        col = example_col1 if i % 2 == 0 else example_col2
        with col:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                prompt = example
                st.rerun()
    
    # 生成ボタン
    st.markdown("---")
    generate_button = st.button(
        "🎨 画像を生成する",
        type="primary",
        use_container_width=True,
        disabled=not api_key or not prompt
    )
    st.divider()
    
    # モデル情報
    st.markdown("### 📊 使用モデル")
    st.info("**Gemini 3 Pro Image**\n\n最新のAI画像生成モデルで、誰でも手軽に高品質な画像を作成できます！")
    
    with st.expander("📖 使い方ガイド"):
        st.markdown("""
        **基本的な使い方:**
        1. Google API キーを入力
        2. 生成したい画像の説明を詳しく入力
        3. 「画像を生成する」ボタンをクリック
        4. 右側のプレビューエリアに画像が表示されます
        
        **プロンプトのコツ:**
        - 詳細な説明を心がける
        - スタイル（水彩画、油絵、リアルなど）を指定
        - 色調や雰囲気を具体的に記述
        - 英語でも日本語でもOK
        """)

# 右カラム: 生成結果のプレビューエリア
with col_right:
    # プレースホルダー
    preview_container = st.container()
    
    with preview_container:
        if not generate_button:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2 style="color: #999;">🖼️ プレビューエリア</h2>
                <p style="color: #666; font-size: 1.1rem;">
                    左側でプロンプトを入力して<br>
                    「画像を生成する」ボタンを押してください
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 画像生成処理
            if not prompt.strip():
                st.error("❌ プロンプトを入力してください。")
            else:
                try:
                    # APIキーを設定してクライアントを初期化
                    client = genai.Client(api_key=api_key)
                    
                    # プログレスバー表示
                    with st.spinner("🍌 AIが思考モードで描画中..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # モデル初期化
                        status_text.text("🔧 Gemini 3 Pro Image モデルを初期化中...")
                        progress_bar.progress(25)
                        time.sleep(0.5)
                        
                        # プロンプトの結合処理
                        if style != "指定なし":
                            final_prompt = f"{style}で、{prompt}を描写してください。"
                        else:
                            final_prompt = prompt
                        
                        # 画像生成リクエスト
                        status_text.text("🎨 AIが画像を生成中... (30秒ほどかかる場合があります)")
                        progress_bar.progress(50)
                        
                        # Gemini 3 Pro Image を使用して画像生成
                        response = client.models.generate_content(
                            model='gemini-3-pro-image-preview',
                            contents=final_prompt
                        )
                        
                        progress_bar.progress(75)
                        status_text.text("✨ 画像を処理中...")
                        time.sleep(0.3)
                        
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
                                    st.image(
                                        pil_image,
                                        caption=f"生成されたプロンプト: {prompt}",
                                        use_container_width=True
                                    )
                                    
                                    # ダウンロードボタン
                                    st.download_button(
                                        label="📥 画像をダウンロード",
                                        data=image_data,
                                        file_name=f"enjoy_banana_{int(time.time())}.png",
                                        mime=mime_type,
                                        use_container_width=True
                                    )
                                    
                                    # 履歴に保存
                                    st.session_state.image_history.append({
                                        'image_data': image_data,
                                        'mime_type': mime_type,
                                        'prompt': prompt,
                                        'timestamp': int(time.time())
                                    })
                                    
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
                        <div class="warning-box">
                            <strong>🔑 APIキーエラー</strong><br>
                            APIキーが無効です。以下を確認してください：<br>
                            • APIキーが正しく入力されているか<br>
                            • APIキーが有効化されているか<br>
                            • Generative AI APIが有効になっているか
                        </div>
                        """, unsafe_allow_html=True)
                    elif "quota" in error_message or "limit" in error_message:
                        st.markdown("""
                        <div class="warning-box">
                            <strong>⚠️ クォータエラー</strong><br>
                            APIの使用制限に達しました。しばらく待ってから再度お試しください。
                        </div>
                        """, unsafe_allow_html=True)
                    elif "safety" in error_message or "blocked" in error_message:
                        st.markdown("""
                        <div class="warning-box">
                            <strong>🛡️ 安全性フィルター</strong><br>
                            プロンプトが安全性フィルターによってブロックされました。<br>
                            別の表現でお試しください。
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("詳細なエラー情報を確認し、プロンプトを変更するか、しばらく待ってから再度お試しください。")

# ギャラリーセクション
if len(st.session_state.image_history) > 0:
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <h2 style="text-align: center; margin-bottom: 2rem;">📜 History / ギャラリー (Ver 3.0)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 履歴を新しい順に表示（逆順）
    history_reversed = list(reversed(st.session_state.image_history))
    
    # 3列でタイル状に表示
    for i in range(0, len(history_reversed), 3):
        cols = st.columns(3)
        
        for j in range(3):
            idx = i + j
            if idx < len(history_reversed):
                item = history_reversed[idx]
                
                with cols[j]:
                    # 画像を表示
                    pil_image = Image.open(io.BytesIO(item['image_data']))
                    st.image(pil_image, use_container_width=True)
                    
                    # プロンプトを表示（短縮）
                    prompt_display = item['prompt'][:50] + "..." if len(item['prompt']) > 50 else item['prompt']
                    st.caption(f"**プロンプト:** {prompt_display}")
                    
                    # タイムスタンプを表示
                    from datetime import datetime
                    timestamp_str = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    st.caption(f"🕐 {timestamp_str}")
                    
                    # ダウンロードボタン
                    st.download_button(
                        label="📥 ダウンロード",
                        data=item['image_data'],
                        file_name=f"generated_image_{len(history_reversed) - idx}.png",
                        mime=item['mime_type'],
                        use_container_width=True,
                        key=f"download_{item['timestamp']}_{idx}"
                    )

# フッター
st.markdown("""
<div class="footer">
    Powered by Nano Banana Pro & Google Generative AI<br>
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
