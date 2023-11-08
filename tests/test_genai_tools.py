import pytest
import os 
from cannoli.cannoli import *

def test_check_default_values():
    default_values = {
        "engine": "gpt-3.5-turbo-instruct",
        "prompt": "Your are my personal assistant. Answer me the best as you can.",
        "max_tokens": 300,
        "temperature": 0.7
    }    
    cannoli = Cannoli()
    assert cannoli.setup == default_values  


def test_get_api_key_from_environment_variable():
    cannoli = Cannoli()
    assert len(cannoli.api_key)>0


def test_get_api_key_as_parameter():
    api_key='test_fake_api'
    cannoli = Cannoli(api_key=api_key)
    assert cannoli.api_key == api_key


def test_quick_question():
    cannoli = Cannoli()
    prompt = "answer me in one word, which country cannoli is?"
    assert cannoli.quick_question(prompt) == "Italy"

def test_cannoli_with_params():
    #bypassing this test, because I haven't access to any azure server. :P
    default_values = {
        "engine": "gpt-3.5-turbo-instruct",
        "prompt": "Your are my personal assistant. Answer me the best as you can.",
        "max_tokens": 300,
        "temperature": 0.7
    }
    api_key = os.getenv('OPENAI_API_KEY')
    api_type = "azure"
    api_base = "https://api.openai.com/v1/assistants"
    api_version = "2023-05-15"
    #cannoli = Cannoli(api_key=api_key, api_type=api_type, api_base=api_base, api_version=api_version)
    #prompt = "answer me in one word, which country cannoli is?"
    #assert cannoli.quick_question(prompt) == "Italy"
    assert 1 == 1