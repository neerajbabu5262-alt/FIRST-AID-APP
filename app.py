import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
st.set_page_config(page_title="First AId", page_icon="🩺", layout="wide")
hide_streamlit_ui = """
            <style>
            /* Hides the top-right menu, deploy button, and GitHub icon */
            [data-testid="stHeader"] {display: none;}
            [data-testid="stToolbar"] {display: none;}
            
            /* Hides the bottom 'Made with Streamlit' footer */
            [data-testid="stFooter"] {display: none;}
            
            /* Attempts to hide the community cloud floating badges */
            #viewerBadge {display: none;}
            .viewerBadge_container {display: none;}
            </style>
            """
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)
def init_db():
    conn = sqlite3.connect('outbreak_radar.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS anonymous_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_category TEXT,
            location TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
def log_anonymous_case(symptom, location):
    if location: 
        conn = sqlite3.connect('outbreak_radar.db')
        c = conn.cursor()
        c.execute('INSERT INTO anonymous_reports (symptom_category, location) VALUES (?, ?)', (symptom, location))
        conn.commit()
        conn.close()
def get_outbreak_alerts():
    conn = sqlite3.connect('outbreak_radar.db')
    query = """
        SELECT symptom_category as Symptom, location as ZipCode, COUNT(*) as CaseCount 
        FROM anonymous_reports 
        GROUP BY symptom_category, location 
        HAVING CaseCount >= 2 
        ORDER BY CaseCount DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
init_db()
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing GEMINI_API_KEY. Please add it to your secrets.toml file.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

system_instructions = """
You are a highly analytical medical triage assistant. Gather information, do NOT immediately diagnose.
Ask 1 or 2 clarifying questions first. Wait for the user to answer. 
Then provide the top 3 potential conditions.
Format your final analysis with ### 🩺 Potential Conditions and ### ⚠️ Next Steps.
Disclaimer: I am an AI, not a doctor.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instructions)


with st.sidebar:
    st.title("First AId 🩺")
    st.caption("AI-powered triage & outbreak radar.")
    
    st.write("---")
    st.write("### 📍 Your Location")
   
    user_location = st.text_input("Enter Zip Code or City:")
    
    if user_location:
        search_query = f"urgent+care+clinics+near+{user_location.replace(' ', '+')}"
        maps_url = f"https://www.google.com/maps/search/{search_query}"
        st.markdown(f"**🏥 [Find Clinics near {user_location}]({maps_url})**")

    st.write("---")
    st.write("### 🚨 Outbreak Radar")
    st.caption("Live, anonymized tracking of local symptoms.")
    
    # Display the database results in a clean table
    alerts_df = get_outbreak_alerts()
    if alerts_df.empty:
        st.success("No localized outbreaks detected currently.")
    else:
        st.warning("⚠️ **Evelated Case Clusters Detected:**")
        st.dataframe(alerts_df, hide_index=True, use_container_width=True)


st.title("Symptom Checker")
st.info("🔒 **Privacy Guarantee:** We do not store your personal data. Only an anonymized symptom category and zip code are sent to the Outbreak Radar.")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    avatar_icon = "🩺" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar_icon):
        st.write(message.parts[0].text)
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Analyzing..."):
            response = st.session_state.chat_session.send_message(user_input)
            st.write(response.text)
            
        
            if user_location:
        
                if "fever" in user_input.lower():
                    log_anonymous_case("Fever", user_location)
                elif "cough" in user_input.lower():
                    log_anonymous_case("Cough", user_location)
                elif "stomach" in user_input.lower() or "nausea" in user_input.lower():
                    log_anonymous_case("Stomach Bug", user_location)
                else:
                    log_anonymous_case("General Pain", user_location)
