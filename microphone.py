import pyaudio
import websockets
import base64
import json
import asyncio
from random import randint
from api_keys import auth_key
from gptInterface import request_api
import functools


from speaker import speakLive


stock_responses = [
    "That's so interesting!",
    "I'm glad you said that. I was thinking the same thing.",
    "Really? That's surprising. Please tell me more.",
    "I'm sorry to hear that. I hope you feel better soon.",
]


FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)


# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f"Connecting websocket to url ${URL}")
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),),
        ping_interval=5,
        ping_timeout=20,
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)

            return True
        
        
        
        async def receive():
            full_transcript = ""  # A state variable to keep track of the full transcript
            
            index_of_charisma = -1 # A state variable to keep track of the index of the last "help me charisma" cue
            while True:
                try:
                    result_str = await _ws.recv()
                    result_json = json.loads(result_str)
                    if result_json["message_type"] == "FinalTranscript":
                        transcript = json.loads(result_str)["text"]
                        transcript_lowercase = (
                            transcript.lower()
                            .replace("?", "")
                            .replace(".", "")
                            .replace("!", "")
                            .replace(",", "")
                        ) + " " # Add a space so "in" works
                        response = None

                        print(f"Transcript: {transcript}")
                        print(transcript_lowercase)
                        print(index_of_charisma)

                        full_transcript += transcript + " "

                        if (
                            "help me charisma" in transcript_lowercase
                            or "help me charisma" == transcript_lowercase
                        ):
                            print(full_transcript)
                            index_of_charisma = full_transcript.lower().index(
                                "charisma"
                            ) + len("charisma")
                            print("index_of_charisma: ", index_of_charisma)
                            # now we're just waiting for the next cue.

                        if "let me think" in transcript_lowercase:
                            text = full_transcript.lower().split("let me think")[0]
                            response = request_api(text, "answer_question", None)

                        if "interesting" in transcript_lowercase:
                            text = full_transcript.lower().split("interesting")[0]
                            response = request_api(text, "continue_conversation", None)

                        # TODO: handle "I wonder if" case. (answer_question)

                        if index_of_charisma != -1:
                            # we have seen the charisma cue before
                            if "what should i ask" in transcript_lowercase:
                                text = (
                                    full_transcript[index_of_charisma:]
                                    .lower()
                                    .split("what should i ask")[0]
                                )
                                response = request_api(
                                    text, "meeting_prep", "generate_questions"
                                )
                                # Mark that we've completed this request.
                                index_of_charisma = -1
                            elif (
                                "what topics should i talk about"
                                in transcript_lowercase
                            ):
                                text = (
                                    full_transcript[index_of_charisma:]
                                    .lower()
                                    .split("what topics should i talk about")[0]
                                )
                                response = request_api(
                                    text, "meeting_prep", "generate_topics"
                                )
                                # Mark that we've completed this request.
                                index_of_charisma = -1
                            elif "what should i know" in transcript_lowercase:
                                text = (
                                    full_transcript[index_of_charisma:]
                                    .lower()
                                    .split("what should i know")[0]
                                )
                                response = request_api(
                                    text, "meeting_prep", "generate_knowledge"
                                )
                                # Mark that we've completed this request.
                                index_of_charisma = -1

                            
                        if response:
                            speakLive(response)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())
