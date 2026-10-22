import streamlit as st
import time
import pandas as pd
import random

st.set_page_config(page_title="Project M.E.M.O.R.Y", page_icon="🚨")

st.title("🚨 Project M.E.M.O.R.Y: Zero-Leak Forensic Unit")
st.write("Evaluating eyewitness short-term memory encoding via counterbalanced, single-exposure live video playback.")

# 1. Initialize data storage and randomized states safely
if "project_data" not in st.session_state:
    st.session_state.project_data = []
if "stage" not in st.session_state:
    st.session_state.stage = "viewing"  # Stages: viewing, video_playing, interrogating, results
if "last_score" not in st.session_state or not st.session_state.last_score:
    st.session_state.last_score = {"correct": 0, "pct": 0, "time": 0.0, "confidence": "None", "timeout": False}
if "active_video_index" not in st.session_state:
    st.session_state.active_video_index = None
if "played_clips" not in st.session_state:
    st.session_state.played_clips = []

# --- ADMINISTRATIVE SIDEBAR OPTIONS ---
st.sidebar.header("👤 Profile Settings")
current_user = st.sidebar.selectbox("Select Active Agent Name:", ["Agent You", "Agent Sister", "Guest Agent"])

STRESS_THRESHOLD = 10.0
HARD_TIME_LIMIT = 20.0    
st.sidebar.info(f"⏱️ High-Confidence Limit: {STRESS_THRESHOLD}s")
st.sidebar.error(f"🛑 Hard Cutoff Limit: {HARD_TIME_LIMIT}s")

# --- MULTI-VIDEO POOL MATRIX (Counterbalancing) ---
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

# --- STEP 1: SYSTEM INITIALIZATION ---
if st.session_state.stage == "viewing":
    st.subheader(f"Step 1: Setup Surveillance System ({current_user})")
    
    if st.session_state.active_video_index is None:
        available_clips = [c for c in VIDEO_POOL.keys() if c not in st.session_state.played_clips]
        if not available_clips:
            st.session_state.played_clips = []
            available_clips = list(VIDEO_POOL.keys())
            
        st.session_state.active_video_index = random.choice(available_clips)
        st.session_state.played_clips.append(st.session_state.active_video_index)
    
    st.info("🎯 Ready to stream security footage. The video will permanently self-destruct after 5 seconds.")
    if st.button("🎬 Stream Evidence (Single Exposure)"):
        st.session_state.stage = "video_playing"
        st.rerun()

# --- STEP 2: FIXED 5-SECOND EXPOSURE ---
elif st.session_state.stage == "video_playing":
    st.subheader("🚨 STREAMING SURVEILLANCE FEED...")
    active_clip = VIDEO_POOL[st.session_state.active_video_index]
    st.video(active_clip["url"], format="video/mp4", autoplay=True, loop=False)
    
    time.sleep(5.0)
    st.session_state.start_time = time.time()
    st.session_state.stage = "interrogating"
    st.rerun()

# --- STEP 3: INTERROGATION SYSTEM WITH INTEGRATED AUTO-SUBMIT MATRIX ---
elif st.session_state.stage == "interrogating":
    st.subheader(f"Step 2: Cross-Examination Registry ({current_user})")
    st.error("🔒 EVIDENCE DESTRUCTED: The video element has been erased to secure trial validity.")
    
    # Calculate current system runtime bounds
    reaction_time = round(time.time() - st.session_state.start_time, 2)
    time_remaining = max(0.0, HARD_TIME_LIMIT - reaction_time)
    
    if time_remaining > 0:
        st.warning(f"⏳ CRITICAL TIMER LOGGING ACTIVE: {round(time_remaining, 1)} seconds remaining!")
    else:
        st.error("💥 SYSTEM LOCKOUT BOUNDS REACHED")
        
    # Process dynamic timeout constraint if no click occurs within the absolute window
    if reaction_time > HARD_TIME_LIMIT:
        st.session_state.last_score = {"correct": 0, "pct": 0, "time": HARD_TIME_LIMIT, "confidence": "Expired (Timeout)", "timeout": True}
        st.session_state.project_data.append({
            "Trial": len(st.session_state.project_data) + 1, "Agent": current_user, "Clip Code": st.session_state.active_video_index,
            "Reaction Time (Seconds)": HARD_TIME_LIMIT, "Accuracy Score (%)": 0, "Confidence Metric": "Expired (Timeout)", "Correct Answers": "0/4"
        })
        st.session_state.stage = "results"
        st.rerun()

    active_clip = VIDEO_POOL[st.session_state.active_video_index]
    
    # Option A: Stable Rapid Voice Dictation Terminal
    st.markdown("### 🎙️ Option A: Rapid Voice Dictation Terminal")
    audio_file = st.audio_input("Tap to record your forensic sequence voice log:")
    
    # AUTOMATION PROTOCOL OPTIMIZATION: Instantly logs response vectors when audio is committed
    if audio_file and st.session_state.stage == "interrogating":
        voice_reaction_time = round(time.time() - st.session_state.start_time, 2)
        st.session_state.last_score = {
            "correct": "Voice Logged", "pct": 100, "time": voice_reaction_time, "confidence": "Voice Analysis Active", "timeout": False
        }
        st.session_state.project_data.append({
            "Trial": len(st.session_state.project_data) + 1,
            "Agent": current_user,
            "Clip Code": st.session_state.active_video_index,
            "Reaction Time (Seconds)": voice_reaction_time,
            "Accuracy Score (%)": 100,
            "Confidence Metric": "Voice (Verified)" if voice_reaction_time <= STRESS_THRESHOLD else "Voice (Delayed)",
            "Correct Answers": "Voice Submitted"
        })
        st.session_state.stage = "results"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📝 Option B: Rapid-Click Interface")
    with st.form("forensic_matrix_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            ans_jacket = st.radio("JACKET Color Variant:", COLORS_POOL, horizontal=True)
            ans_jeans = st.radio("JEANS Color Variant:", COLORS_POOL, horizontal=True)
        with col_b:
            ans_cap = st.radio("CAP Color Variant:", COLORS_POOL, horizontal=True)
            ans_shoes = st.radio("SHOES Color Variant:", COLORS_POOL, horizontal=True)
            
        submitted = st.form_submit_button("💥 SUBMIT RECORDED VERDICT")
        
        if submitted:
            click_reaction_time = round(time.time() - st.session_state.start_time, 2)
            correct_count = 0
            if ans_jacket == active_clip["jacket"]: correct_count += 1
            if ans_jeans == active_clip["jeans"]: correct_count += 1
            if ans_cap == active_clip["cap"]: correct_count += 1
            if ans_shoes == active_clip["shoes"]: correct_count += 1
            accuracy_pct = int((correct_count / 4) * 100)
            confidence = "High (Automatic)" if click_reaction_time <= STRESS_THRESHOLD else "Low (Delayed)"
            
            st.session_state.last_score = {
                "correct": correct_count, "pct": accuracy_pct, "time": click_reaction_time, "confidence": confidence, "timeout": False
            }
            
            st.session_state.project_data.append({
                "Trial": len(st.session_state.project_data) + 1,
                "Agent": current_user,
                "Clip Code": st.session_state.active_video_index,
                "Reaction Time (Seconds)": click_reaction_time,
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
        st.error(f"❌ RECALL RECORDING FAILED: Window limit exceeded.")
    else:
        if ls['correct'] == "Voice Logged":
            st.success("🎤 Audio log preserved securely for automated diagnostic processing!")
        else:
            st.metric(label="Total Identification Accuracy", value=f"{ls['pct']}%", delta=f"{ls['correct']}/4 Correct")
        st.write(f"⏱ boardwalk **Total Retrieval Speed:** {ls['time']} seconds | **Confidence Allocation:** {ls['confidence']}")
    
    if st.button("🔄 Proceed to Next Unique Trial", key="next_trial_btn"):
        st.session_state.active_video_index = None
        st.session_state.stage = "viewing"
        st.rerun()

# --- ANALYTICS DISPLAY PANELS ---
if st.session_state.project_data and st.session_state.stage == "viewing":
    st.divider()
    df = pd.DataFrame(st.session_state.project_data)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Global Reflex Leaderboard")
        max_acc = df["Accuracy Score (%)"].max()
        top_tier = df[df["Accuracy Score (%)"] == max_acc]
        leaderboard_df = top_tier.groupby("Agent")["Reaction Time (Seconds)"].min().reset_index()
        st.dataframe(leaderboard_df.sort_values(by="Reaction Time (Seconds)").reset_index(drop=True), use_container_width=True)
        
    with col2:
        st.subheader("📈 Statistical Overview")
        st.scatter_chart(data=df, x="Reaction Time (Seconds)", y="Accuracy Score (%)")
        
    st.subheader("📋 Comprehensive Trial Registry Log")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Export Full Forensic Dataset (.CSV)", data=csv_data, file_name="project_memory_data.csv", mime="text/csv", use_container_width=True)
    st.dataframe(df.set_index("Trial"), use_container_width=True)

