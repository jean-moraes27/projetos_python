import moviepy.editor

video = moviepy.editor.VideoFileClip("banho_dos_campeoes.mp4")

audio_data = video.audio

audio_data.write_audiofile("audio_banho_dos_campeoes.mp3")