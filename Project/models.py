from langchain import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import argostranslate.translate
import scipy
import numpy as np


from utils import extract_chapter_text, extract_decisions


def LLM_pure(llm, prompt):
    longchat_template = f"""### System: 
    Use a friendly tone, rich descriptions.
    {history}
    ### User: 
    {input}
    ### Assistant:
    """
    
    longchat_prompt_template = PromptTemplate(input_variables=["history", "input"], template=longchat_template)
    
    conversation_buf = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory(ai_prefix="Assistant", human_prefix="User"),
        prompt=longchat_prompt_template,
    )
    return conversation_buf(prompt)["response"]

def LLM_story(conv_buf, prompt, mode):
    response = conv_buf(prompt)["response"]
    
    if mode == "story":
        chapter_title, text = extract_chapter_text(response)
        return conv_buf, chapter_title, text
    else:
        decisions = extract_decisions(response)
        return conv_buf, decisions


def SDXL(sdxl, llm, response, chap, decision):
    prompt = LLM_pure(llm, response + "\nCreate a text-to-image prompt that aligns perfectly with the provided text, focus on extracting key themes, visual elements, and emotions from the text, and translate these into a detailed, imaginative, and vivid description that encapsulates the essence of the narrative for an image generation AI.")
    n_steps = 30
    image = sdxl(
        prompt=prompt,
        num_inference_steps=n_steps,
    ).images[0]
    #image
    path = f'images/result_chap{chap}_{decision}.png'
    image.save(path)
    
    return path


def TL(text, from_code = "en", to_code = "en"):
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    
    return translatedText


def TTM(ttm, llm, response, chap, decision):
    negative_prompt = """Avoid low quality, muddled sounds, dissonance, erratic rhythms, harsh dynamics, high frequencies."""
    prompt = LLM_pure(llm, response + "\nInstruct a text-to-music AI to compose a piece that resonates with the given text, convey the story's mood, setting, and emotional undertones in concise terms, highlighting key elements like pace, genre, and instruments that mirror the narrative's ambiance.")
    # run the generation
    audio = ttm(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=200,
        audio_length_in_s=30.0
    ).audios
    
    audio_int = np.int16(audio[0] / np.max(np.abs(audio)) * 32767)
    path = f"sounds/result_chap{chap}_{decision}.wav"
    scipy.io.wavfile.write(path, rate=16000, data=audio_int)
    
    return path