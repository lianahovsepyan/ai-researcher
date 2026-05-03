import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage

# Էջի դիզայնը
st.set_page_config(page_title="Liana's AI Lab", page_icon="🧪")
st.title("🧪 Liana's Agentic Research Lab")
st.markdown("Այս Agent-ը ինքնուրույն փնտրում է տվյալներ ինտերնետում և կատարում վերլուծություն։")

# API Keys-ի մուտքագրում Sidebar-ում
with st.sidebar:
    st.header("🔑 Մուտքանուններ")
    gemini_key = st.text_input("Enter Gemini API Key", type="password")
    tavily_key = st.text_input("Enter Tavily API Key", type="password")
    st.info("Tavily Key-ն կարող ես ստանալ tavily.com կայքից (անվտանգ է և անվճար):")

if gemini_key and tavily_key:
    os.environ["GOOGLE_API_KEY"] = gemini_key
    os.environ["TAVILY_API_KEY"] = tavily_key
    
    # Մոդելների սահմանում
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    search_tool = TavilySearchResults(k=3) # Որոնում է 3 լավագույն արդյունքները

    topic = st.text_input("Ի՞նչ թեմա հետազոտենք:", "AI in Physics 2026")

    if st.button("Սկսել Հետազոտությունը"):
        with st.status("🕵️ Agent-ը աշխատում է...", expanded=True) as status:
            
            # Քայլ 1: Որոնում
            st.write("🔍 Ինտերնետում որոնում ենք թարմ տվյալներ...")
            # Tavily-ն վերադարձնում է լիստ, մենք այն դարձնում ենք մեկ տեքստ
            search_results = search_tool.run(f"latest technical updates 2026 on {topic}")
            st.write("✅ Տվյալները հավաքված են։")
            
            # Քայլ 2: Վերլուծություն
            st.write("🧠 Վերլուծում ենք տեղեկատվությունը...")
            res_msg = [
                SystemMessage(content="Դու Senior Researcher ես: Վերլուծիր տրված տվյալները հայերենով և պատրաստիր մանրամասն հաշվետվություն:"),
                HumanMessage(content=f"Թեմա: {topic}\n\nՏվյալներ: {search_results}")
            ]
            summary = llm.invoke(res_msg).content
            
            status.update(label="Հետազոտությունը ավարտված է!", state="complete", expanded=False)

        # Արդյունքների ցուցադրում
        st.subheader("📊 Հետազոտության Արդյունք")
        st.markdown(summary)
else:
    st.warning("⚠️ Խնդրում եմ տեղադրիր Gemini և Tavily API բանալիները ձախ կողմում:")