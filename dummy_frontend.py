import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Skyfly Lead Dashboard", layout="wide")
st.title("🚀 Skyfly Technology - Lead Dashboard")

base_url = st.text_input("Backend URL", "https://skyfly-calling-ai-agent-production.up.railway.app").rstrip("/")

if st.button("🔄 Refresh Leads List"):
    try:
        resp = requests.get(f"{base_url}/view-leads", timeout=10)
        data = resp.json()
        
        if data and isinstance(data, list):
            df = pd.DataFrame(data)
            # Sirf wahi columns dikhayenge jo zaroori hain
            display_df = df.rename(columns={
                "customer_name": "Name",
                "service_interested": "Service",
                "contact_info": "Contact",
                "budget": "Budget",
                "created_at": "Date/Time"
            })
            st.dataframe(display_df[["Name", "Service", "Contact", "Budget", "Date/Time"]], use_container_width=True)
            st.success(f"Total {len(data)} leads captured.")
        else:
            st.info("Abhi tak koi leads nahi hain.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

st.divider()
st.subheader("➕ Manual Lead Entry")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Client Name")
    service = st.selectbox("Service Required", ["Web Dev", "AI Voice Agent", "E-commerce", "SEO"])
with col2:
    contact = st.text_input("Phone/Email")
    budget = st.text_input("Estimated Budget")

if st.button("Save Manual Lead"):
    if name and contact:
        payload = {"name": name, "service": service, "contact": contact, "budget": budget}
        try:
            r = requests.post(f"{base_url}/collect-lead", json=payload)
            if r.status_code == 200:
                st.success("Lead Saved! Refresh kar ke check karein.")
            else:
                st.error("Failed to save.")
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Name and Contact are required.")
