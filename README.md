# First AId 🩺
**AI-Powered Medical Triage & Local Outbreak Radar**

First AId is a privacy-first, conversational symptom checker built to bridge the gap between initial medical concerns and professional care. Rather than functioning as a standard chat bot, the application acts as an interactive triage assistant—asking clarifying questions before providing non-diagnostic information and directing users to nearby medical facilities. 

### 🚀 Core Features
* **Stateless Triage Chat:** Powered by Gemini 2.5 Flash, the AI conducts an interactive interview to analyze symptoms without ever storing the user's personal conversational data.
* **Privacy-First Architecture:** Built with a strict ephemeral state. The conversational memory is permanently wiped the moment the browser tab is closed or refreshed.
* **Live Outbreak Radar:** An anonymized early-signal detection system backed by SQLite. It silently tracks broad symptom categories by zip code to detect and alert users to localized illness clusters (e.g., flu spikes).
* **Location Integration:** Instantly generates dynamic Google Maps queries to help users find the nearest urgent care clinics based on their zip code.

### 🛠️ Tech Stack
* **Frontend/Middleware:** Python, Streamlit, Pandas
* **AI Engine:** Google Generative AI (Gemini 2.5 Flash API)
* **Database:** SQLite (Anonymized Data Aggregation)
