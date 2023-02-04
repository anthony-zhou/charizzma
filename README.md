# charizzma

docker run -v /Users/anthony/Documents/GitHub/charizzma:/project -it --entrypoint /bin/bash --device /dev/snd:/dev/snd bot

docker build . --tag bot --platform linux/amd64