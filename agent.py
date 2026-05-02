
import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

# Էջի դիզայնը
st.set_page_config(page_title="Liana's AI Lab", page_icon="🧪")
st.title("🧪 Liana's Agentic Research Lab")
st.markdown("Այս Agent-ը ինքնուրույն փնտրում է տվյալներ ինտերնետում և կատարում վերլուծություն։")

# API Key մուտքագրում (անվտանգության համար)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    wrapper = DuckDuckGoSearchAPIWrapper()
    search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)
    topic = st.text_input("Ի՞նչ թեմա հետազոտենք:", "AI in Physics 2026")

    if st.button("Սկսել Հետազոտությունը"):
        with st.status("🕵️ Agent-ը աշխատում է...", expanded=True) as status:
            
            # Քայլ 1: Որոնում
            st.write("🔍 Ինտերնետում որոնում ենք թարմ տվյալներ...")
            raw_data = search_tool.run(f"latest technical updates 2026 on {topic}")
            st.write("✅ Տվյալները հավաքված են։")
            
            # Քայլ 2: Վերլուծություն
            st.write("🧠 Վերլուծում ենք տեղեկատվությունը...")
            res_msg = [
                SystemMessage(content="Դու Senior Researcher ես: Ամփոփիր այս տվյալները:"),
                HumanMessage(content=raw_data)
            ]
            summary = llm.invoke(res_msg).content
            
            status.update(label="Հետազոտությունը ավարտված է!", state="complete", expanded=False)

     
     
        # Արդյունքների ցուցադրում
        st.subheader("📊 Հետազոտության Արդյունք")
        st.markdown(summary)
else:
    st.info("Խնդրում եմ տեղադրիր քո API Key-ն ձախ կողմում՝ սկսելու համար։")