import openai
import api_keys

openai.api_key = api_keys.openai_api_key

PROMPTS = {
    "continue_conversation": "You are a charismatic conversation assistant. I am speaking with a friend and I will give you our conversation history below. Please give me a good one or two sentence response that will continue the conversation.",
    "answer_question": " You are a truthful question answering system. I was asked the question given below. Give an appropriate response.",
}


def request_api(conv_text, conv_type):
    print("Calling API...")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{PROMPTS[conv_type]}\n{conv_text}\n",
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1,
    )

    return response
