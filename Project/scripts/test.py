from init import init_LLM_PURE, init_LLM_STORY, init_SDXL, init_Translator, init_TTM
from models import LLM_story, SDXL, TL, TTM
from utils import ordinal, check_GPU
import logging

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"


# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
check_GPU()
LLM_PURE_ = init_LLM_PURE()
TTM_ = init_TTM()
sound_path = TTM(TTM_, LLM_PURE_, "text", chap=1, decision=1)

fsefs
#SDXL_ = init_SDXL()
language_dict = init_Translator()
TTM_ = init_TTM()
# def init_models():
#     LLM_PURE_ = init_LLM_PURE()
#     SDXL_ = init_SDXL
#     language_dict = init_Translator
#     TTM_ = init_TTM
#     
#     return LLM_PURE_, SDXL_, TTM_
# Current memory usage
import torch
allocated_memory = torch.cuda.memory_allocated(0) / 1024**2  # Convert to MB
print(f"  Allocated Memory: {allocated_memory:.2f} MB")
def start_gen(Params, LLM_PURE_): # after configuration page, while reading the prolog
    #update Params
    keys_to_update = ["main_name", "gender"]
    for key in keys_to_update:
        if key in Params:
            Params[key] = TL(Params[key], from_code=Params["language"])
    
    LLM_STORY_ = init_LLM_STORY(LLM_PURE_, Params)
    
    LLM_STORY_, chapter, text = LLM_story(LLM_STORY_, "Write now only the 1st chapter!", mode="story") # type: ignore
    # print(chapter)
    # print(text)
    LLM_STORY_, decisions = LLM_story(LLM_STORY_, f"Create now {Params['num_decisions']} decisions how the story could continue.", mode="decisions") # type: ignore
    # print(decisions)
    
    image_path = SDXL(SDXL_, LLM_PURE_, text, chap=1, decision=1)
    sound_path = TTM(TTM_, LLM_PURE_, text, chap=1, decision=1)
    
    language = Params["language"]
    return LLM_STORY_, TL(text, to_code=language), TL(chapter, to_code=language), TL(decisions, to_code=language), image_path, sound_path
def next_gen(Params, LLM_STORY_, LLM_PURE_, chap_num, decision):
    LLM_STORY_, chapter, text = LLM_story(LLM_STORY_, f"Write now the {ordinal(chap_num)} chapter of {params['NUM_CHAPTERS']} with using decision {decision}.", mode="story") # type: ignore
    LLM_STORY_, decisions = LLM_story(LLM_STORY_, f"Create now {Params['num_decisions']} decisions how the story could continue.", mode="decisions") # type: ignore
    
    image_path = SDXL(SDXL_, LLM_PURE_, text, chap_num, decision)
    sound_path = TTM(TTM_, LLM_PURE_, text, chap_num, decision)
    
    language = Params["language"]
    return LLM_STORY_, TL(text, to_code=language), TL(chapter, to_code=language), TL(decisions, to_code=language), image_path, sound_path
params = {}
params["main_name"] = "Klaus"
params["gender"] = "Männlich"
params["language"] = "de"
params["num_decisions"] = 4
params["num_chapters"] = 5

LLM_STORY_, cur_story, chapter_title, decisions, image_path, sound_path = start_gen(params, LLM_PURE_)
print(cur_story)
print(chapter_title)
print(decisions)
print(image_path)
print(sound_path)