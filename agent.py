import streamlit as st
import os
import google.generativeai as genai
from langchain_community.tools.tavily_search import TavilySearchResults

st.set_page_config(page_title="Liana's AI Lab", page_icon="🧪")
st.title("🧪 Liana's Agentic Research Lab")

with st.sidebar:
    st.header("🔑 Մուտքանուններ")
    gemini_key = st.text_input("Enter Gemini API Key", type="password")
    tavily_key = st.text_input("Enter Tavily API Key", type="password")

if gemini_key and tavily_key:
    try:
        genai.configure(api_key=gemini_key)
        # Մոդելի սահմանումը՝ առանց models/ նախդիրի
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        os.environ["TAVILY_API_KEY"] = tavily_key
        search_tool = TavilySearchResults(k=3)

        topic = st.text_input("Ի՞նչ թեմա հետազոտենք:", "AI in Physics 2026")

        if st.button("Սկսել Հետազոտությունը"):
            with st.status("🕵️ Agent-ը աշխատում է...", expanded=True) as status:
                # Քայլ 1: Որոնում
                st.write("🔍 Ինտերնետում որոնում ենք...")
                search_results = search_tool.run(topic)
                
                # Քայլ 2: Վերլուծություն
                st.write("🧠 Վերլուծում ենք տվյալները...")
                prompt = f"Analyze these search results and provide a detailed report in Armenian about: {topic}. Results: {search_results}"
                
                response = model.generate_content(prompt)
                
                status.update(label="Ավարտված է!", state="complete", expanded=False)
                st.subheader("📊 Հետազոտության Արդյունք")
                st.markdown(response.text)
    except Exception as e:
        st.error(f"Տեղի է ունեցել սխալ: {e}")
else:
    st.warning("⚠️ Խնդրում եմ տեղադրիր API բանալիները:")