import os
import openai
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
api_base = os.environ.get('OPENAI_API_BASE')
if api_key is not '':
    openai.api_key = api_key
if api_base is not '':
    openai.api_base = api_base

def translate_text(system_prompt,input_text):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_text}
    ],
    timeout=999
    )
    translations = completion.choices[0].message
    return translations

input_file = """
你现在是一个中英翻译大师，帮我把所有输入的英文翻译成中文
"""

translated_text = translate_text(input_file,"hello").content
print(translated_text)

