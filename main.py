import os
import re
from openai import OpenAI
import argparse
import json
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
parser=argparse.ArgumentParser(description='Translate string for i18n')
parser.add_argument('--folder', required=True,help='Path to the src folder of the website')
parser.add_argument('--language',required=True, help='Target language name (e.g. french, german)')
args=parser.parse_args()
def extract_strings_from_file(file_path):
    jsx_strings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        jsx_regex = r'<(?:\w+\s[^>]*?\s*|\/)?>(.*?)<\/\w+>'
        matches = re.findall(jsx_regex, content, re.DOTALL)
        for match in matches:
            text_content = match.strip()
            if '{' not in text_content and '}' not in text_content:
                jsx_strings.append(text_content)
        return jsx_strings

def extract_strings_from_codebase(codebase_dir):
    all_strings = []
    for root, _, files in os.walk(codebase_dir):
        for file in files:
            if file.endswith('.jsx') or file.endswith('.js') or file.endswith('.astro'):
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
        text = text.strip()
        if text:
            readable_text.append(text)
    return readable_text

codebase_dir = args.folder
language=args.language
text_strings = extract_strings_from_codebase(codebase_dir)
readable_text=extract_readable_text(text_strings)

client=OpenAI(
    api_key=api_key
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful translator assistant fluent in most lanugages designed to output JSON."},
    {"role": "user", "content": f"Can you please translate the list of strings given below to {language}"},
    {"role":"user","content":"Also, omit HTML, CSS, JS, React and other Web Development keywords from translation"},
    {"role":"user","content":"Give me only the translated text as a list of individual strings, I do not need the originals"},
    {"role":"user","content":"".join(readable_text)}
  ]
)

Translation=response.choices[0].message.content
json_filepath=f'{language}_translation.json'
with open(json_filepath,'w', encoding="UTF-8") as f:
    json.dump(Translation,f,ensure_ascii=False, indent=4)