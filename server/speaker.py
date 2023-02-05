import os, boto3

defaultRegion = "us-east-1"
defaultUrl = "https://polly.us-east-1.amazonaws.com"


def connectToPolly(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client("polly", region_name=regionName, endpoint_url=endpointUrl)


def speak(polly, text, format="mp3", voice="Brian"):
    text = f"<speak><prosody rate=\"fast\">{text}</prosody></speak>"
    resp = polly.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice, TextType="ssml")
    soundfile = open("/tmp/sound.mp3", "wb")
    soundBytes = resp["AudioStream"].read()
    soundfile.write(soundBytes)
    soundfile.close()
    os.system("afplay /tmp/sound.mp3")  # Works only on Mac OS, sorry
    os.remove("/tmp/sound.mp3")


def speakLive(text):
    polly = connectToPolly()
    speak(polly, text)
