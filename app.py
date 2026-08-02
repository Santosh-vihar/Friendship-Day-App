"""
Friendship Day Celebration App for Vihar
-----------------------------------------
Main Streamlit entry point.
Deploy as: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
import shutil

from modules.database import init_db, check_visitor, save_visitor, update_visitor_video
from modules.ui import (load_css, landing_header, show_balloons_html, show_confetti,
                        photo_question_ui, celebration_page, video_preview_page,
                        welcome_back_page)
from modules.video_generator import create_slideshow
from modules.helpers import generate_id

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="Friendship Day - Vihar",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----- LOAD CSS -----
load_css()

# ----- INITIALISE DATABASE -----
init_db()

# ----- SESSION STATE INITIALISATION -----
defaults = {
    "step": 1,               # 1: landing, 2: photo question, 3: upload, 4: celebration, 5: video preview
    "first_name": "",
    "surname": "",
    "full_name": "",
    "existing_user": False,
    "photo_choice": None,
    "uploaded_photos": [],
    "video_path": None,
    "generation_done": False
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ----- STEP 1: LANDING PAGE (NAME INPUT) -----
if st.session_state.step == 1 and not st.session_state.existing_user:
    # Animated balloons and confetti on landing
    landing_header()
    show_balloons_html()
    show_confetti()

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("## 👋 Enter Your Name", unsafe_allow_html=True)
            with st.form("name_form"):
                first = st.text_input("First Name", placeholder="e.g., Rahul")
                surname = st.text_input("Surname", placeholder="e.g., Sharma")
                submitted = st.form_submit_button("Celebrate Now 🎉")

                if submitted:
                    if not first.strip() or not surname.strip():
                        st.error("Please enter both your first name and surname.")
                    else:
                        fn = first.strip().title()
                        sn = surname.strip().title()
                        full = f"{fn} {sn}"
                        # check database
                        exists, _ = check_visitor(fn, sn)
                        if exists:
                            st.session_state.existing_user = True
                            st.session_state.full_name = full
                            st.session_state.first_name = fn
                            st.session_state.surname = sn
                            st.rerun()
                        else:
                            # new visitor
                            save_visitor(fn, sn, full, datetime.now().isoformat(), False, "")
                            st.session_state.first_name = fn
                            st.session_state.surname = sn
                            st.session_state.full_name = full
                            st.session_state.step = 2
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ----- EXISTING USER WELCOME BACK -----
if st.session_state.existing_user:
    welcome_back_page(st.session_state.full_name)
    st.stop()

# ----- STEP 2: PHOTO QUESTION -----
if st.session_state.step == 2:
    photo_question_ui()
    # Buttons handled inside ui function, set step 3 or 4 and rerun

# ----- STEP 3: UPLOAD PHOTOS -----
if st.session_state.step == 3:
    st.markdown(f"## Upload Memorable Photos with Vihar, {st.session_state.first_name} ❤️")
    st.markdown("### Please upload between 3 and 5 photos (JPG, PNG, JPEG)")

    uploaded = st.file_uploader(
        "Choose photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="photo_uploader"
    )

    if uploaded:
        st.session_state.uploaded_photos = uploaded
        count = len(uploaded)
        if count < 3:
            st.warning(f"You have uploaded {count} photo(s). Please upload at least 3.")
        elif count > 5:
            st.warning("You can upload a maximum of 5 photos. Please remove some.")
        else:
            st.success(f"{count} photos uploaded! Ready to create your Friendship Day video.")
            if st.button("✨ Generate My Friendship Day Video", type="primary", use_container_width=True):
                with st.spinner("Creating your beautiful video... This may take a moment."):
                    # Save uploaded photos temporarily
                    temp_dir = Path("database/temp_photos") / generate_id()
                    temp_dir.mkdir(parents=True, exist_ok=True)
                    saved_paths = []
                    for idx, img_file in enumerate(st.session_state.uploaded_photos):
                        ext = Path(img_file.name).suffix
                        safe_name = f"photo_{idx+1}{ext}"
                        dest = temp_dir / safe_name
                        with open(dest, "wb") as f:
                            f.write(img_file.getbuffer())
                        saved_paths.append(str(dest))

                    # Generate video
                    output_dir = Path("database/generated_videos")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    video_name = f"{st.session_state.full_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
                    output_path = output_dir / video_name

                    try:
                        create_slideshow(
                            image_paths=saved_paths,
                            name=st.session_state.full_name,
                            output_path=str(output_path)
                        )
                        # Update database with video filename
                        update_visitor_video(st.session_state.first_name, st.session_state.surname, video_name)
                        st.session_state.video_path = str(output_path)
                        st.session_state.generation_done = True
                        st.session_state.step = 5
                        # Cleanup temp photos
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        st.rerun()
                    except Exception as e:
                        st.error(f"An error occurred while generating the video: {e}")
                        shutil.rmtree(temp_dir, ignore_errors=True)

# ----- STEP 4: CELEBRATION PAGE (NO PHOTOS) -----
if st.session_state.step == 4:
    celebration_page(st.session_state.full_name)

# ----- STEP 5: VIDEO PREVIEW & DOWNLOAD -----
if st.session_state.step == 5 and st.session_state.video_path:
    video_preview_page(st.session_state.full_name, st.session_state.video_path)
