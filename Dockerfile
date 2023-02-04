FROM pytorch/pytorch

# Install dependencies
RUN apt update && apt-get install ffmpeg -y
RUN pip install openai
RUN apt install gcc -y
RUN apt install pulseaudio -y
RUN apt-get install portaudio19-dev -y
RUN pip install pyaudio
# add install open api
