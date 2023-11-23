import openai 
from dataclasses import dataclass, field
import os
import sys
import json
import glob 
from pathlib import Path

@dataclass
class Cannoli:
    api_key: str = field(default=None)
    api_type: str = field(default=None)
    api_base: str = field(default=None)
    api_version: str = field(default=None)    
    setup: dict = field(default=None)
    last_prompt: str = field(default='')
    response: dict = field(default=None)

    def __post_init__ (self):
        self.openai = openai
        if not self.setup:
            self.load_default_settings()
        if self.api_type:
            self.openai.api_type = self.api_type
        if self.api_base:
            self.openai.api_base = self.api_base
        if self.api_version:
            self.openai.api_version = self.api_version
        if not self.api_key:
            self.get_api_key()
        self.openai.api_key = self.api_key

        
        

    def load_default_settings(self):
        try:
            # tenta abrir o arquivo no caminho do codigo
            setup_filename = glob.glob(os.path.join('.', 'default_settings.json'))
            # senao, tenta abrir um arquivo padrao
            if not setup_filename:
                setup_filename = Path(__file__).resolve().parent / 'default_settings.json'
            else:
                setup_filename = setup_filename[0]
            
            with open(setup_filename, 'r', encoding='utf-8') as settings_file:
                self.setup = json.load(settings_file)
        except Exception:
            raise

    def get_api_key(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("'Error: OPENAI_API_KEY is missing. Please, include it in your initiatlization script.'")

    def __parse_response(self, response):
        if response.get('error'):
            print(f"API Error - response['error']['message']: {response['error']['message']}")
            return None
        generated_text = response.choices[0].text.strip()
        return generated_text


    def api_request(self, prompt=None):
        if prompt: 
            self.last_prompt = '' if not self.setup.get('prompt') else self.setup.get('prompt') 
            self.setup['prompt'] = prompt

        create = self.openai.ChatCompletion.create if self.api_type else self.openai.Completion.create
        self.response = create(**self.setup)
        return self.response

    def quick_question(self, prompt):
        self.api_request(prompt)
        return self.__parse_response(self.response)


def main():
    # making quick questions
    demo = Cannoli()
    #api_key='sdf'
    #api_type='azure'
    #api_base='google.com/'
    #api_version='23-11-23'

    #demo = Cannoli(api_key=api_key, api_type=api_type, api_base=api_base, api_version=api_version)
    ans = demo.quick_question("what is a cannoli?")
    print(ans)

    # accessing the full response
    print(demo.response)

    # accessing the last prompt
    demo.quick_question('who is gandalf?')
    print(demo.last_prompt)


if __name__ == "__main__":
    main()