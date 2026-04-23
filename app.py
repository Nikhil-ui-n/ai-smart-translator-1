import os
import streamlit as st
import google.generativeai as genai

# ====== CONFIG ======
st.set_page_config(page_title="Smart Code Translator", layout="wide")

st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
textarea { background-color: #1e1e1e !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.title("💻 Smart Code Translator (Gemini)")

# ====== API KEY ======
API_KEY = os.getenv("AIzaSyBzNvWXM77Qs2ldd_F-B_hPHfSR3ONkRco")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Set it using environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ====== SIDEBAR ======
st.sidebar.title("⚙️ Settings")

action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

# ====== INPUT ======
code = st.text_area("📝 Paste your code here:", height=300)

# ====== PROMPT BUILDER ======
def generate_prompt():
    if action == "Translate Code":
        return f"""
Translate this {source_lang} code to {target_lang}.
Only return the code. No explanation.

Code:
{code}
"""
    elif action == "Explain Code":
        return f"""
Explain this {source_lang} code in simple beginner-friendly language.

Code:
{code}
"""
    elif action == "Optimize Code":
        return f"""
Optimize this {source_lang} code.

Return:
1. Optimized code
2. Improvements

Code:
{code}
"""
    elif action == "Analyze Complexity":
        return f"""
Analyze time and space complexity of this {source_lang} code.

Return:
- Time Complexity
- Space Complexity
- Explanation

Code:
{code}
"""

# ====== RUN ======
if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("⚠️ Please enter code!")
    else:
        with st.spinner("Processing..."):
            try:
                prompt = generate_prompt()
                response = model.generate_content(prompt)
                result = response.text

                st.success("✅ Done!")
                st.subheader("📌 Output")
                st.code(result, language=target_lang.lower())

                st.download_button("⬇️ Download Output", result, file_name="output.txt")
                st.text_area("📋 Copy Output", result, height=150)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
