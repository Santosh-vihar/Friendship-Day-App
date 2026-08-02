"""
Slideshow video generator using MoviePy.
Creates a Friendship Day video with Ken Burns effect, crossfades, and text overlays.
"""

from moviepy.editor import (
    ImageClip, concatenate_videoclips, CompositeVideoClip,
    TextClip, AudioClip
)
from moviepy.video.fx.all import resize, fadein, fadeout
import numpy as np
from pathlib import Path

def _create_silent_audio(duration: float) -> AudioClip:
    """Generate a silent audio clip of given duration."""
    def make_frame(t):
        return np.zeros((1, 2))  # 2 channels, zero amplitude
    return AudioClip(make_frame, duration=duration, fps=44100)

def create_slideshow(image_paths: list[str], name: str, output_path: str,
                     bg_music_path: str = None, duration_per_image: float = 3.0,
                     crossfade_duration: float = 1.0):
    """
    Generate a Friendship Day slideshow video.
    
    Args:
        image_paths: list of image file paths (3-5 images)
        name: full name of the person (for title overlays)
        output_path: where to save the MP4 file
        bg_music_path: optional background music file path; if None, silent audio is used
    """
    clips = []
    img_duration = duration_per_image
    fade_dur = crossfade_duration

    # Create image clips with Ken Burns zoom effect
    for img_path in image_paths:
        clip = (ImageClip(img_path)
                .set_duration(img_duration)
                .resize(lambda t: 1 + 0.05 * t)  # subtle zoom-in
                .set_position('center'))
        # Add crossfade (fadein/fadeout will be applied later via concatenation)
        clips.append(clip)

    # Concatenate with crossfade
    video = concatenate_videoclips(clips, method="compose",
                                   padding=-fade_dur)  # negative padding gives overlap crossfade

    # --- Text overlays ---
    # Title at the beginning (first 2 seconds)
    txt_title = (TextClip(f"Happy Friendship Day, {name}",
                          fontsize=60, color='white', font='Liberation-Sans',
                          stroke_color='black', stroke_width=2, method='label')
                 .set_duration(2)
                 .set_position('center')
                 .crossfadein(0.5))

    # End message (last 3 seconds)
    # We'll position it relative to the end by using video.duration
    end_msg = (TextClip(f"Thank you, {name} ❤️\nFrom Vihar",
                        fontsize=50, color='white', font='Liberation-Sans',
                        stroke_color='black', stroke_width=2, method='label',
                        align='center')
               .set_duration(3)
               .set_position('center')
               .crossfadein(0.5))

    # Composite text over the main video
    # To place end message at the end, we set its start time = video.duration - 3
    final_video = CompositeVideoClip([
        video,
        txt_title.set_start(0),
        end_msg.set_start(video.duration - 3)
    ])

    # --- Audio ---
    if bg_music_path and Path(bg_music_path).exists():
        audio = AudioClip.from_file(bg_music_path).subclip(0, final_video.duration)
        audio = audio.volumex(0.3)  # lower volume
    else:
        audio = _create_silent_audio(final_video.duration)

    final_video = final_video.set_audio(audio)

    # Write output
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        threads=4,
        preset='medium',
        verbose=False,
        logger=None
    )
