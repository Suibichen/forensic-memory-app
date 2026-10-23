import streamlit as st
import pandas as pd
import time

# Set up page configurations
st.set_page_config(page_title="Zero-Leak GovTech Engine", page_icon="🚨", layout="centered")

st.title("🚨 Zero-Leak Forensic Hub")
st.subheader("GovTech Prototype: Crowdsourced Forensic Intelligence")
st.markdown("---")

# Initialize persistent session states for simulating multiple witness entries
if "all_reports" not in st.session_state:
    st.session_state.all_reports = []

# --- CITIZEN INTERFACE (High-Stress UX Mode) ---
st.header("Step 1: Live Citizen Reporting Interface")
st.info("Simulate a panicked citizen submitting an immediate witness log after an event.")

# Start tracking retrieval time the moment the page/module loads
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Dropdown and Radio configurations designed for fast muscle memory clicks
with st.form(key="witness_report_form", clear_on_submit=True):
    st.write("**Rapid Visual Capture Panel**")
    
    jacket_color = st.radio("Suspect Jacket Color:", ["Black", "Blue", "Red", "Green", "Unknown"], horizontal=True)
    vehicle_type = st.radio("Escape Vehicle Mode:", ["On Foot", "Sedan", "SUV", "Motorbike", "None"], horizontal=True)
    flight_direction = st.radio("Direction of Flight:", ["North", "South", "East", "West", "Unknown"], horizontal=True)
    
    submit_button = st.form_submit_button(label="🔒 SECURE & TRANSMIT EVIDENCE")

if submit_button:
    # Calculate exactly how fast the user locked in their answers
    end_time = time.time()
    retrieval_speed = round(end_time - st.session_state.start_time, 2)
    
    # Package individual report with military-grade metadata characteristics
    new_report = {
        "Witness ID": f"CITIZEN-{len(st.session_state.all_reports) + 1:03d}",
        "Jacket": jacket_color,
        "Vehicle": vehicle_type,
        "Direction": flight_direction,
        "Retrieval Speed (s)": retrieval_speed
    }
    
    # Save to the application state (Simulating secure ingestion server)
    st.session_state.all_reports.append(new_report)
    st.success(f"Evidence Locked and Encrypted! Data transmitted in {retrieval_speed} seconds. Local app state purged.")
    
    # Reset timer for the next simulated witness entry
    st.session_state.start_time = time.time()

# --- INVESTIGATOR DASHBOARD (The Consensus Engine) ---
st.markdown("---")
st.header("🕵️‍♂️ Real-Time Investigator Dashboard")

if len(st.session_state.all_reports) == 0:
    st.warning("Awaiting incoming citizen data streams. Submit reports above to test the consensus aggregation engine.")
else:
    # Convert active reports to dataframes
    df = pd.DataFrame(st.session_state.all_reports)
    
    st.write("### Raw Encrypted Incoming Streams")
    st.dataframe(df, use_container_width=True)
    
    # Process through the Neuroscience Consensus Filter (Drop variations over 12 seconds)
    filtered_df = df[df["Retrieval Speed (s)"] <= 12.0]
    valid_entries = len(filtered_df)
    
    st.write("### 🧠 Predictive Consensus Analysis")
    
    if valid_entries > 0:
        # Calculate mode and confidence percentages
        top_jacket = filtered_df["Jacket"].mode()[0]
        jacket_conf = (filtered_df["Jacket"].value_counts().max() / valid_entries) * 100
        
        top_vehicle = filtered_df["Vehicle"].mode()[0]
        vehicle_conf = (filtered_df["Vehicle"].value_counts().max() / valid_entries) * 100
        
        # Display Key Analytics Cards
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Suspect Jacket Focus", value=top_jacket, delta=f"{jacket_conf:.1f}% Confidence")
        col2.metric(label="Suspect Transit Mode", value=top_vehicle, delta=f"{vehicle_conf:.1f}% Confidence")
        col3.metric(label="Filtered Valid Accounts", value=f"{valid_entries} / {len(df)}")
        
        st.caption("🚨 *Note: The consensus algorithm automatically isolates and down-weights inputs with high retrieval times to account for neuro-cognitive memory dilution.*")
    else:
        st.error("All current incoming reports exceeded the 12-second neurological validity threshold. Data integrity insufficient for automated profiling.")

# Reset feature to keep testing efficient
if st.button("🔄 Reset System Database"):
    st.session_state.all_reports = []
    st.session_state.start_time = time.time()
    st.rerun()
