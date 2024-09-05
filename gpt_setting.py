import os
import re

from utils import *
from llm_settings.openai_models import *
from llm_settings.gemini_models import *
from llm_settings.deepinfra_models import *


def print_prompt(inputs, response):
    os.makedirs("records", exist_ok=True)
    with open(f"records/records.txt", 'a') as f:
        f.write(f"{inputs}\n----\n")
        f.write(f"{response}\n====\n")
    return


def llm_request(model, inputs):    
    if model.startswith("gpt"):
        response = gpt_chat(model, inputs).strip()
    
    elif model.startswith("gemini"):
        response = gemini_chat(model, inputs).strip()
    
    elif model.startswith("meta-llama"):
        response = deepinfra_chat(model, inputs).strip()
    
    else:
        raise ValueError("The model is not supported or does not exist.")
    
    print_prompt(inputs, response)
    
    return response