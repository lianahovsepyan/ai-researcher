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
    st.info("Tavily Key-ն կարող ես ստանալ tavily.com կայքից:")

if gemini_key and tavily_key:
    # Tavily-ին տալիս ենք Key-ն environment-ի միջոցով
    os.environ["TAVILY_API_KEY"] = tavily_key
    
    # 1. ԿԱՐԵՎՈՐ ՓՈՓՈԽՈՒԹՅՈՒՆ: Gemini-ին տալիս ենք Key-ն ուղղակիորեն
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_key  # Այս տողը ավելացրինք
    )
    
    search_tool = TavilySearchResults(k=3)

    topic = st.text_input("Ի՞նչ թեմա հետազոտենք:", "AI in Physics 2026")

    if st.button("Սկսել Հետազոտությունը"):
        with st.status("🕵️ Agent-ը աշխատում է...", expanded=True) as status:
            
            st.write("🔍 Ինտերնետում որոնում ենք թարմ տվյալներ...")
            # 2. Tavily-ն կանչում ենք ճիշտ ձևով
            try:
                search_results = search_tool.run(topic)
                st.write("✅ Տվյալները հավաքված են։")
                
                st.write("🧠 Վերլուծում ենք տեղեկատվությունը...")
                res_msg = [
                    SystemMessage(content="Դու Senior Researcher ես: Վերլուծիր տրված տվյալները հայերենով:"),
                    HumanMessage(content=f"Թեմա: {topic}\n\nՏվյալներ: {search_results}")
                ]
                summary = llm.invoke(res_msg).content
                
                status.update(label="Հետազոտությունը ավարտված է!", state="complete", expanded=False)
                
                st.subheader("📊 Հետազոտության Արդյունք")
                st.markdown(summary)
            except Exception as e:
                st.error(f"Տեղի է ունեցել սխալ: {e}")
else:
    st.warning("⚠️ Խնդրում եմ տեղադրիր Gemini և Tavily API բանալիները ձախ կողմում:")