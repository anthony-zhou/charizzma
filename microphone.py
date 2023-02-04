import pyaudio
import websockets
import base64
import json
import asyncio
from random import randint
from api_keys import auth_key

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
            while True:
                try:
                    result_str = await _ws.recv()
                    result_json = json.loads(result_str)
                    if result_json["message_type"] == "FinalTranscript":
                        text = json.loads(result_str)["text"]
                        print(text)
                        if "Lemme think" in text or "Let me think" in text:
                            response = stock_responses[
                                randint(0, len(stock_responses) - 1)
                            ]
                            speakLive(response)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())
