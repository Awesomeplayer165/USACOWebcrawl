import ollama
import csv
from datetime import datetime
import csv
import json

allJson = {}

def generate_code(): 
    global allJson
    sourceFile = open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_ollama_out.json', 'w')
    with open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems_phase1.csv', mode ='r') as file:
        count = 0
        csvFile = csv.reader(file)
        for lines in csvFile:
            if count == 0:
                count += 1
                continue;
            message = lines[1] + '. do NOT provide any explanation EXCEPT the code formatted in markdown without noting the language. The code generated MUST be in python.'
            startTime = datetime.now()
            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': message}],
            )
            endTime = datetime.now()
            timeSpent = (endTime - startTime).total_seconds()
            print(f'Problem {count} on {lines[0]}: Time Spent Generating: {timeSpent} seconds')
            count += 1

            code = response['message']['content']
            code.replace('\n', '')
            code.replace('"', '')
            code.replace("'", '')

            append_to_json(lines[0], {
                "code": code,
                "time_gen": f'\ntime generating: {timeSpent}s'
            })

    sourceFile.close()

def append_to_json(key, value: dict):
    with open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_ollama_out.json', 'w') as file:
        allJson[key] = value
        file.write(json.dumps(allJson))
        

def read_code():
    with open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_ollama_out.json', 'r') as file:
        data = json.load(file)
        print(len(data))
#generate_code()
read_code()
