# Charizzma, HackBU 2023 Submission

Charizzma aids users by offering quick and meaningful insights into a conversation. Charizzma uses AssemblyAI's speach recognition functionality to turn spoken word into text that is parsed and passed into GPT-3 when cues are given. When AssemblyAI recognizes a natural cue, it passes a custom-engineered prompt to GPT-3, which returns textual insight into the conversation. Finally, we use Amazon's speech-to-text tooling to give the client appropriate insight into whatever they requested. In the future, we are considering diarization features that would give GPT-3 a better understanding of the conversation, enabling it to give more intelligent insights. 


How to run:

docker run -v /Users/anthony/Documents/GitHub/charizzma:/project -it --entrypoint /bin/bash --device /dev/snd:/dev/snd bot

docker build . --tag bot --platform linux/amd64

