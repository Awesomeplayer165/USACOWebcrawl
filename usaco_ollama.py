import ollama
import csv
from datetime import datetime

sourceFile = open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_ollama_out.txt', 'w')

with open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems_phase1.csv', mode ='r') as file:
    count = 0
    csvFile = csv.reader(file)
    for lines in csvFile:
        if count == 0:
            count += 1
            continue;
        message = lines[1] + '. do NOT provide any explanation EXCEPT the code formatted in markdown without noting the language. The code generated MUST be in python.'
        startTime = datetime.now()
        stream = ollama.chat(
                model='llama3',
            messages=[{'role': 'user', 'content': message}],
            stream=True,
        )
        print(lines[0], file = sourceFile)
        print("\n", file = sourceFile)
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True, file = sourceFile)
        endTime = datetime.now()
        timeSpent = (endTime - startTime).total_seconds()
        print(f'Problem {count}: Time Spent Generating: {timeSpent} seconds')
        print(f"\ntime generating: {timeSpent}s", file = sourceFile) 
        count += 1
        print(file = sourceFile)
        print("------------------------------------------------", file = sourceFile)

sourceFile.close()
