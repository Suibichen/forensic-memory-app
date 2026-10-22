import streamlit as st
import time
import pandas as pd
import random

st.set_page_config(page_title="Project M.E.M.O.R.Y", page_icon="🚨")

st.title("🚨 Project M.E.M.O.R.Y: Live Video Forensic Unit")
st.write("Evaluating eyewitness short-term memory encoding via counterbalanced, single-exposure live video playback.")

# 1. Initialize data storage and randomized states safely
if "project_data" not in st.session_state:
    st.session_state.project_data = []
if "stage" not in st.session_state:
    st.session_state.stage = "viewing"  # Stages: viewing, interrogating, results
if "last_score" not in st.session_state or not st.session_state.last_score:
    st.session_state.last_score = {"correct": 0, "pct": 0, "time": 0.0, "confidence": "None", "timeout": False}
if "active_video_index" not in st.session_state:
    st.session_state.active_video_index = None

# --- ADMINISTRATIVE SIDEBAR OPTIONS ---
st.sidebar.header("👤 Profile & Thresholds")
current_user = st.sidebar.selectbox("Select Active Agent Name:", ["Agent You", "Agent Sister", "Guest Agent"])
STRESS_THRESHOLD = st.sidebar.slider("High-Confidence Time Limit (Seconds)", 3.0, 10.0, 8.0)

HARD_TIME_LIMIT = 20.0
st.sidebar.error(f"🛑 CRITICAL TIME BOUND: {HARD_TIME_LIMIT}s")

# --- NEW: MULTI-VIDEO POOL MATRIX TO ELIMINATE ORDER EFFECTS ---
# Replace these URLs with your real hosted raw .mp4 clip links!
VIDEO_POOL = {
    "Clip_A": {
        "url": "https://github.com/Suibichen/forensic-memory-app/raw/refs/heads/main/Security%20Camera%20Alleyway%20Chase.mp4", # Replace with your original clip link
        "jacket": "Red", "jeans": "Blue", "cap": "Black", "shoes": "Green"
    },
    "Clip_B": {
        "url": "https://github.com/Suibichen/forensic-memory-app/raw/refs/heads/main/Alleyway%20Chase.mp4", # Replace with Video Variant 2 link
        "jacket": "Blue", "jeans": "Black", "cap": "Green", "shoes": "Red"
    },
    "Clip_C": {
        "url": "https://github.com/Suibichen/forensic-memory-app/raw/refs/heads/main/Screen_Recording_20261022_202310_Chrome.mp4", # Replace with Video Variant 3 link
        "jacket": "Green", "jeans": "Red", "cap": "Blue", "shoes": "Black"
    }
}

COLORS_POOL = ["Black", "Blue", "Red", "Green"]

# --- STEP 1: LIVE VIDEO VIEWING ---
if st.session_state.stage == "viewing":
    st.subheader(f"Step 1: Analyze the Evidence ({current_user})")
    
    # Randomly select a video clip configuration at the start of the trial loop
    if st.session_state.active_video_index is None:
        st.session_state.active_video_index = random.choice(list(VIDEO_POOL.keys()))
        
    active_clip = VIDEO_POOL[st.session_state.active_video_index]
    
    st.markdown("### 🎬 Surveillance Footage Feed")
    st.warning("⚠️ COUNTERBALANCED MATRIX ACTIVE: The clothing configurations change dynamically per trial to reduce memory order bias.")
    
    # Streams the randomly chosen video clip file flawlessly
    st.video(active_clip["url"], format="video/mp4", autoplay=True, loop=False)
    
    st.info("Once the clip finishes playing, click the button below instantly to open the case matrix.")
    
    if st.button("🚨 Advance to High-Pressure Interrogation"):
        st.session_state.start_time = time.time()
        st.session_state.stage = "interrogating"
        st.rerun()

# --- STEP 2: HIGH-PRESSURE INTERROGATION ---
elif st.session_state.stage == "interrogating":
    st.subheader(f"Step 2: Cross-Examination Registry ({current_user})")
    st.error("🔒 FOOTAGE SEQUESTERED: The surveillance video has been completely scrubbed from the view layout.")
    
    st.markdown("### 🎙️ Option A: Rapid Voice Dictation Terminal")
    audio_file = st.audio_input("Tap to speak your forensic sequence (e.g., 'Red Blue Black Green'):")
    if audio_file:
        st.success("🗣️ Voice segment recorded successfully! Processing audio logs...")

    st.markdown("---")
    st.markdown("### 📝 Option B: Rapid-Click Interface")
    
    # Retrieve the locked truth answers for whichever random clip played in Step 1
    active_clip = VIDEO_POOL[st.session_state.active_video_index]
    TRUE_JACKET = active_clip["jacket"]
    TRUE_JEANS = active_clip["jeans"]
    TRUE_CAP = active_clip["cap"]
    TRUE_SHOES = active_clip["shoes"]
    
    with st.form("forensic_matrix_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            ans_jacket = st.radio("JACKET Variant:", COLORS_POOL, horizontal=True)
            ans_jeans = st.radio("JEANS Variant:", COLORS_POOL, horizontal=True)
        with col_b:
            ans_cap = st.radio("CAP Variant:", COLORS_POOL, horizontal=True)
            ans_shoes = st.radio("SHOES Variant:", COLORS_POOL, horizontal=True)
            
        submitted = st.form_submit_button("💥 SUBMIT FORENSIC VERDICT")
        
        if submitted:
            end_time = time.time()
            reaction_time = round(end_time - st.session_state.start_time, 2)
            
            # Enforce 20-second hard ceiling logic rule
            if reaction_time > HARD_TIME_LIMIT:
                accuracy_pct, correct_count = 0, 0
                confidence = "Expired (Timeout)"
                timeout_flag = True
                logged_time = HARD_TIME_LIMIT
            else:
                timeout_flag = False
                logged_time = reaction_time
                correct_count = 0
                if ans_jacket == TRUE_JACKET: correct_count += 1
                if ans_jeans == TRUE_JEANS: correct_count += 1
                if ans_cap == TRUE_CAP: correct_count += 1
                if ans_shoes == TRUE_SHOES: correct_count += 1
                accuracy_pct = int((correct_count / 4) * 100)
                confidence = "High (Automatic)" if reaction_time <= STRESS_THRESHOLD else "Low (Delayed)"
            
            st.session_state.last_score = {
                "correct": correct_count, "pct": accuracy_pct, "time": reaction_time, "confidence": confidence, "timeout": timeout_flag
            }
            
            st.session_state.project_data.append({
                "Trial": len(st.session_state.project_data) + 1,
                "Agent": current_user,
                "Clip Used": st.session_state.active_video_index,
                "Reaction Time (Seconds)": logged_time,
                "Accuracy Score (%)": accuracy_pct,
                "Confidence Metric": confidence,
                "Correct Answers": f"{correct_count}/4"
            })
            st.session_state.stage = "results"
            st.rerun()

# --- STEP 2b: FEEDBACK SCREEN ---
elif st.session_state.stage == "results":
    st.subheader("Step 2b: Interrogation Analysis Summary")
    ls = st.session_state.last_score
    
    if ls.get("timeout", False):
        st.error(f"❌ CRITICAL TIMEOUT: Response took {ls['time']}s! Real-life memory degradation threshold surpassed.")
    else:
        st.metric(label="Total Identification Accuracy", value=f"{ls['pct']}%", delta=f"{ls['correct']}/4 Correct")
        st.write(f"⏱️ **Total Retrieval Speed:** {ls['time']} seconds | **Confidence Allocation:** {ls['confidence']}")
    
    if st.button("🔄 Proceed to Next Unique Trial", key="next_trial_btn"):
        # Reset the index pointer so a completely new random clip is pulled for the next run
        st.session_state.active_video_index = None
        st.session_state.stage = "viewing"
        st.rerun()

# --- STEP 3: ANALYTICS & LEADERBOARD DISPLAY ---
if st.session_state.project_data and st.session_state.stage != "interrogating":
    st.divider()
    df = pd.DataFrame(st.session_state.project_data)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Global Reflex Leaderboard")
        max_acc = df["Accuracy Score (%)"].max()
        top_tier = df[df["Accuracy Score (%)"] == max_acc]
        leaderboard_df = top_tier.groupby("Agent")["Reaction Time (Seconds)"].min().reset_index()
        leaderboard_df = leaderboard_df.sort_values(by="Reaction Time (Seconds)").reset_index(drop=True)
        leaderboard_df.index = leaderboard_df.index + 1
        st.dataframe(leaderboard_df, use_container_width=True)
        
    with col2:
        st.subheader("📈 Statistical Overview")
        st.scatter_chart(data=df, x="Reaction Time (Seconds)", y="Accuracy Score (%)")
        
    st.subheader("📋 Comprehensive Trial Registry Log")
    
    # NEW: Formatted CSV Data Download Trigger Hook Option
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Forensic Dataset (.CSV)",
        data=csv_data,
        file_name="project_memory_data.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.dataframe(df.set_index("Trial"), use_container_width=True)

# --- SYSTEM CACHE WIPE TOOL ---
st.markdown("---")
if st.button("🧹 Wipe System State Cache (Reset All Data)", use_container_width=True):
    st.session_state.project_data = []
    st.session_state.active_video_index = None
    st.session_state.stage = "viewing"
    st.session_state.last_score = {"correct": 0, "pct": 0, "time": 0.0, "confidence": "None", "timeout": False}
    st.toast("System cache cleared successfully!", icon="🧹")
    st.rerun()
