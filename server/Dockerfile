FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Install dependencies
RUN apt update && apt-get install ffmpeg -y
RUN apt install gcc -y
RUN apt install pulseaudio -y
RUN apt-get install portaudio19-dev -y

# COPY requirements.txt /opt/app/requirements.txt
# WORKDIR /opt/app
# RUN pip install -r requirements.txt

RUN pip install openai
RUN pip install websockets
RUN pip install boto3
RUN pip install pyaudio
RUN pip install firebase-admin
# add install open api
