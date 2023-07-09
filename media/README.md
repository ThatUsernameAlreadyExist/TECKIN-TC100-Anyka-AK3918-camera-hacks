To convert audio: ffmpeg -i IN.wav -acodec pcm_s16le -ar 8000 -ac 1 OUT.wav

Batch file converting:
  Windows CMD:
    FOR /F "tokens=*" %G IN ('dir /b *.wav') DO ffmpeg -i "%G" -acodec pcm_s16le -ar 8000 -ac 1 "8-%~nG.wav"
