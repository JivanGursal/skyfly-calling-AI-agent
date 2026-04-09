import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Skyfly Technology - Lead Dashboard", layout="wide")

st.title("🚀 Skyfly Technology Lead Management")
st.subheader("AI Voice Agent se aayi hui leads yahan dikhengi")

# Backend URL (Railway ka URL yahan daalein)
base_url = st.text_input("Backend URL", "https://your-railway-app.com").rstrip("/")

st.divider()

# Leads Fetch karne ka button
if st.button("Refresh Leads List"):
    try:
        # Humne backend mein /view-leads banaya tha (ya fir /list_appointments jaisa logic)
        resp = requests.get(f"{base_url}/view-leads", timeout=10)
        resp.raise_for_status()
        leads_data = resp.json()

        if leads_data:
            df = pd.DataFrame(leads_data)
            # Column names ko thoda saaf dikhane ke liye
            df.columns = [col.replace('_', ' ').title() for col in df.columns]
            st.dataframe(df, use_container_width=True)
            st.success(f"Total {len(leads_data)} leads found!")
        else:
            st.info("Abhi tak koi leads nahi aayi hain.")
            
    except Exception as e:
        st.error(f"Error fetching leads: {e}")

st.sidebar.markdown("""
### Quick Actions
- [x] Check Web Dev Leads
- [x] Check AI Voice Leads
- [x] Follow up with clients
""")
