from langchain import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import sys
from opennsfw_standalone import OpenNSFWInferenceRunner
import argostranslate.translate
import scipy
import numpy as np
import logging
import torch
import os
from PIL import Image
from pydub import AudioSegment

torch.cuda.set_device(0)


from utils import (extract_chapter_text, extract_decisions, find_best_matching_mood, 
                   get_mood_from_path, generate_story_prompt, generate_decision_prompt)


def LLM_pure(llm, prompt):
    logging.info("Starting LLM_pure function")
    longchat_template = """### System: 
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
    logging.info("LLM_pure function completed")
    return conversation_buf(prompt)["response"]

def LLM_story(conv_buf, prompt, mode, llm):
    logging.info("Starting LLM_story function")
    response = conv_buf(prompt)["response"]
    
    if mode == "story":
        for i in range(11):
            chapter_title, text = extract_chapter_text(response, i)
            prompt = generate_story_prompt(response, chapter_title, text)
            is_valid = LLM_pure(llm, prompt)
            if is_valid:
                logging.info("LLM_story function completed")
                return conv_buf, chapter_title, text
            else:
                logging.info("Extraction wasn't working, try another pattern.")
    else:
        for i in range(10):
            decisions = extract_decisions(response, i)
            prompt = generate_decision_prompt(response, decisions)
            is_valid = LLM_pure(llm, prompt)
            if is_valid:
                logging.info("LLM_story function completed")
                return conv_buf, decisions
            else:
                logging.info("Extraction wasn't working, try another pattern.")

    logging.info("LLM_story function completed with no valid extraction")
    return None  # or any default value indicating no valid extraction


def SDXL(sdxl, detector, llm, response, chap, decision):
    logging.info("Starting SDXL function")
    max_retry = 4  # if the image don't pass the check
    for i in range(max_retry):
        prompt = LLM_pure(llm, response + "\nCreate a text-to-image prompt that aligns perfectly with the provided text, focus on extracting key themes, visual elements, and emotions from the text, and translate these into a detailed, imaginative, and vivid description that encapsulates the essence of the narrative for an image generation AI. Write not more than 50 words.")
        n_steps = 30
        
        image = sdxl(
            prompt,
            num_inference_steps=n_steps,
        ).images[0]
        
        if not os.path.exists('images'):
            os.makedirs("images")
        path = f'images/result_chap{chap}_{decision}.png'
        image.save(path)
        
        # Load the image as bytes
        with open(path, 'rb') as image_file:
            image_data = image_file.read()
        
        # Run NSFW detection
        nsfw_score = detector.infer(image_data)
        
        # Check if the NSFW score is above a certain threshold
        if nsfw_score < 0.2:  
            logging.info(f"NSFW not detected, NSFW Score: {nsfw_score}")
            return path
        else:
            logging.info(f"NSFW Detected, creating a new image, NSFW Score: {nsfw_score}")
            response = LLM_pure(llm, response + "\nRevise the story in a way that is suitable for children.")
            # If this is the last retry, return the path of the previous image
            if i+1 == max_retry:
                return f'images/result_chap{chap-1}_{decision}.png'


def TL(text, from_code = "en", to_code = "en"):
    logging.info("Starting TL function")
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    logging.info("TL function completed")
    
    return translatedText


def TTM(ttm, llm, response, chap, decision, prev_sounds=[], use_ai_music=True):
    logging.info("Starting TTM function")
    if use_ai_music:
        logging.info("Generating music")
        negative_prompt = """Avoid low quality, muddled sounds, dissonance, erratic rhythms, harsh dynamics, high frequencies."""
        prompt = LLM_pure(llm, response + "\nInstruct a text-to-music AI to compose a piece that resonates with the given text, convey the story's mood, setting, and emotional undertones in concise terms, highlighting key elements like pace, genre, and instruments that mirror the narrative's ambiance. Write not more than 100 words.")
        # run the generation
        audio = ttm(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=200,
            audio_length_in_s=30.0
        ).audios
        
        # Convert to pydub AudioSegment for easy manipulation
        audio_segment = AudioSegment(
            np.int16(audio[0] / np.max(np.abs(audio)) * 32767).tobytes(), 
            frame_rate=16000, 
            sample_width=2, 
            channels=1
        )
        
        # Apply fade in and fade out (2 seconds each)
        faded_audio = audio_segment.fade_in(2000).fade_out(2000)
        
        # Ensure the 'sounds' directory exists
        if not os.path.exists('sounds'):
            os.makedirs("sounds")

        path = f"sounds/result_chap{chap}_{decision}.wav"
        
        # Export the modified audio
        faded_audio.export(path, format="wav")
        
        logging.info("TTM function completed")
        
        return path
    else:
        logging.info("Choosing music")
        
        # Get the moods of the previous two sounds
        previous_moods = [get_mood_from_path(sound, predefined_songs) for sound in prev_sounds if sound]
        
        # Prepare a list of available moods, excluding the previous ones
        available_moods_arr = [mood for mood in predefined_songs.keys() if mood not in previous_moods]
        available_moods = ", ".join(available_moods_arr)
        mood_prompt = f"Based on the following text, choose the a fitting mood from the following options: {available_moods}. Be creative by choosing. Text: {response}"
        llm_response = LLM_pure(llm, mood_prompt)  # This should return a mood like 'happy', 'sad', etc.
        
        # Find the best matching mood
        chosen_mood = find_best_matching_mood(llm_response, predefined_songs.keys())

        if chosen_mood:
            song_path = predefined_songs[chosen_mood]
            logging.info("TTM function completed")
            return song_path
        else:
            logging.warning("No valid mood found in the LLM response")
            logging.info("TTM function completed")
            return None

predefined_songs = {
    "Charming and Whimsical": "My Little Toys.wav",
    "Cute and Playful": "Precious Childhood Moments.wav",
    "Peaceful and Calming": "Making Waffles.wav",
    "Energetic and Joyful": "Sunny Popcorn Fields.wav",
    "Festive and Celebratory": "Happy Jazzy Birthday!.wav",
    "Fun and Quirky": "Mister Clumsy.wav",
    "Whimsical and Light": "Balloon Waltz.wav",
    "Lilting and Calming": "Got Some Brand New Toys.wav",
    "Comedic and Playful": "Happy Funny Kids Children Music.wav",
    "Youthful and Entertaining": "A Ticket To Childhood.wav",
    "Uplifting and Motivational": "A Day to Remember.wav",
    "Quirky and Fun": "A Dog's Life.wav",
    "Friendly and Joyful": "Friends Forever.wav",
    "Playful and Energetic": "Candy Town.wav",
    "Lighthearted and Amusing": "Dogs and Cats.wav",
    "Bright and Inspirational": "Flowers in your Hair.wav",
    "Adventurous and Dynamic": "Horse Race.wav",
    "Festive and Celebratory": "Funny Party.wav",
    "Whimsical and Imaginative": "Weird Toys.wav",
    "Encouraging and Positive": "Make It Happen.wav"
    # Add more entries as needed
}