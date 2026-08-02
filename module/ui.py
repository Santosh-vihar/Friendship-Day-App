"""
UI components, CSS injection, and animations.
"""

import streamlit as st
from pathlib import Path

def load_css():
    """Inject custom CSS from styles/style.css."""
    css_file = Path(__file__).parent.parent / "styles" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Google Fonts import
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

def landing_header():
    """Display the main title and subtext."""
    st.markdown("""
    <div class="landing-header">
        <h1 class="title">🎈 Happy Friendship Day 🎈</h1>
        <p class="subtitle">Celebrate the bond of friendship with <span class="highlight">Vihar</span></p>
    </div>
    """, unsafe_allow_html=True)

def show_balloons_html():
    """Inject floating balloon CSS animations."""
    # Multiple balloon elements with random positions and delays
    balloons_html = "".join([
        f'<div class="balloon" style="left: {i*12}%; animation-delay: {i*0.3}s;"></div>'
        for i in range(8)
    ])
    st.markdown(f'<div class="balloon-container">{balloons_html}</div>', unsafe_allow_html=True)

def show_confetti():
    """Trigger confetti animation using canvas-confetti library."""
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    setTimeout(() => {
        confetti({
            particleCount: 200,
            spread: 80,
            origin: { y: 0.5 }
        });
    }, 500);
    </script>
    """, unsafe_allow_html=True)

def photo_question_ui():
    """Ask user if they have photos, with large buttons."""
    st.markdown(f"## Hi {st.session_state.first_name}! 😊")
    st.markdown("### Do you have memorable photos with Vihar?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes ❤️", use_container_width=True, key="btn_yes"):
            st.session_state.photo_choice = True
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("No 😊", use_container_width=True, key="btn_no"):
            st.session_state.photo_choice = False
            st.session_state.step = 4
            st.rerun()

def celebration_page(name: str):
    """Show a rich celebration page with animations, hearts, and a quote."""
    show_balloons_html()
    show_confetti()
    st.balloons()  # built-in Streamlit balloons

    st.markdown(f"""
    <div class="celebration-card">
        <h1>🎉 Happy Friendship Day, {name} ❤️</h1>
        <div class="hearts-container">
            <span class="floating-heart">❤️</span>
            <span class="floating-heart">💖</span>
            <span class="floating-heart">💕</span>
            <span class="floating-heart">💝</span>
            <span class="floating-heart">💗</span>
        </div>
        <p class="quote">
            "True friendship isn't about being inseparable.<br>
            It's about being apart and nothing changes."
        </p>
        <p class="author">– Unknown</p>
    </div>
    """, unsafe_allow_html=True)

def video_preview_page(name: str, video_path: str):
    """Show the generated video with download button and celebration effects."""
    show_confetti()
    st.balloons()
    st.markdown(f"## 🎬 Your Friendship Day Video, {name}!")
    st.video(video_path)
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    st.download_button(
        label="⬇️ Download Video",
        data=video_bytes,
        file_name=f"Friendship_Day_{name.replace(' ', '_')}.mp4",
        mime="video/mp4",
        use_container_width=True
    )
    st.success("Thank you for celebrating with Vihar! 🥳")

def welcome_back_page(name: str):
    """Display for returning visitors."""
    show_balloons_html()
    show_confetti()
    st.balloons()
    st.markdown(f"""
    <div class="welcome-back-card">
        <h1>🎉 Welcome back, {name}! 🎉</h1>
        <p class="welcome-msg">
            You are already a friend of Vihar and have already<br>
            celebrated Friendship Day here. ❤️
        </p>
        <p class="friend-emoji">🤝✨💫</p>
    </div>
    """, unsafe_allow_html=True)
