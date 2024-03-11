import os
import re
import openai
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client=OpenAI(
    api_key=api_key
)


def extract_strings_from_file(file_path):
    jsx_strings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # jsx_regex=r'>([^<]+)<'
        jsx_regex = r'<(?:\w+\s[^>]*?\s*|\/)?>(.*?)<\/\w+>'
        matches = re.findall(jsx_regex, content, re.DOTALL)
        for match in matches:
            text_content = match.strip()
            if '{' not in text_content and '}' not in text_content and len(text_content)>0:
                jsx_strings.append(text_content)
        return jsx_strings

def extract_strings_from_codebase(codebase_dir):
    all_strings = []
    for root, _, files in os.walk(codebase_dir):
        for file in files:
            if file.endswith('.jsx') or file.endswith('.js') or file.endswith('.astro') or file.endswith('.md'):
                file_path = os.path.join(root, file)
                strings = extract_strings_from_file(file_path)
                all_strings.extend(strings)
    return all_strings

def extract_readable_text(strings):
    readable_text = []
    for string in strings:
        text = re.sub(r'<[^>]+>', '', string)
        text = re.sub(r'{[^}]+}', '', text)
        text = re.sub(r'\/\/.*\n', '', text)
        text = re.sub(r'\/\*.*\*\/', '', text)
        text = re.sub(r'\/\*.+\*\/', '', text)
        text = re.sub(r'<!--.*-->', '', text)
        text = re.sub(r'<svg[^>]+>', '', text)
        text = re.sub(r'<path[^>]+>', '', text)
        text = re.sub(r'<g[^>]+>', '', text)
        text = re.sub(r'<a[^>]+>', '', text)
        text = re.sub(r'<title[^>]+>', '', text)
        text = re.sub(r'<li[^>]+>', '', text)
        text = re.sub(r'<h[0-9][^>]*>', '', text)
        text = re.sub(r'<div[^>]*>', '', text)
        text = re.sub(r'className="[^"]*"', '', text)
        text=re.sub(r'^import.*\n?', '', text)
        text = text.strip()
        if text:
            readable_text.append(text)
    return readable_text

def convert_strings_to_JSON(client, readable_text):
    json_object = {f"key{i}": string for i, string in enumerate(readable_text, 1)}
    # Convert the dictionary to a JSON formatted string
    json_str = json.dumps(json_object, indent=4)
    print(json_str)
    return json_str


def chat_and_translate(client, language, readable_text):
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful translator assistant fluent in most lanugages designed to output a list of JSON strings of text"},
            {"role":"user","content":"Given a JSON object of key value pairs, can you please translate the values to the given language below."},
            {"role": "user", "content": f"Can you please translate the list of strings given below to {language}"},
            {"role":"user","content":"Also, omit HTML, CSS, JS, React and other Web Development keywords from translation"},
            {"role":"user","content":f"the JSON object already has unique keys, please do not change the keys, only translate the values."},
            {"role":"user","content":"".join(readable_text)}
        ]
        )
        return response
    except openai.APIError as error:
        return error.code

    

def create_translated_json(response, language, dest_path):
    Translation=json.loads(response.choices[0].message.content)
    json_filepath=dest_path+f'/{language}_translation.json'
    with open(json_filepath,'w', encoding="UTF-8") as f:
        json.dump(Translation,f,ensure_ascii=False, indent=4)

def main_function(codebase__dir, language, dest):
    text_strings = extract_strings_from_codebase(codebase__dir)
    readable_text=extract_readable_text(text_strings)
    response1=convert_strings_to_JSON(client, readable_text)
    # print(response1.choices[0].message.content)
    response=chat_and_translate(client, language, response1)
    create_translated_json(response, language, dest)
