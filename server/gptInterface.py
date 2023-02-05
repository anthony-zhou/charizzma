import openai
from api_keys import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY

PROMPTS = {
    "continue_conversation": "You are a charismatic conversation assistant. I am speaking with a friend and I will give you our conversation history below. Please give me a good one or two sentence response that will continue the conversation.",
    "meeting_prep": {
        "base": "You are a charismatic conversation assistant. I will provide you with details on an upcoming meeting, such as the person I am meeting, their interests, and their recent experiences.",
        "generate_questions": "Your role is to give 5 detailed questions that will continue the conversation.",
        "generate_topics": "Your role is to give 5 detailed topics that will continue the conversation.",
        "generate_context": "Your role is to give me sufficient context for the conversation.",
    },
    "answer_question": "You are a truthful question answering system. I was asked the question given below. Give an appropriate response.",
}


def request_api(conv_text, conv_type, cue_sub):
    print("Calling API...")

    ##depending on prompt, create prompts differently
    if conv_type == "meeting_prep":
        base_prompt = PROMPTS[conv_type]["base"]
        sub_prompt = PROMPTS[conv_type][cue_sub]
        generated_prompt = f"{base_prompt}{sub_prompt}{conv_text}"
    else:
        generated_prompt = f"{PROMPTS[conv_type]}\n{conv_text}\n"

    print("API called with arguments: ", conv_text, conv_type, cue_sub)
    print("Generated prompt: ", generated_prompt)

    response = "This is a test response."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generated_prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1,
    )

    return response['choices'][0]['text']
