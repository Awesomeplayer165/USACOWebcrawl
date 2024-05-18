import json

problems = json.loads(open('/Users/jacobtrentini/Development/USACOWebcrawl/usaco_ollama_out.json', 'r').read())

# get selenium to sign in to usaco with my credentials

from selenium import webdriver
from selenium.webdriver.common.by import By

wd = webdriver.Firefox()

wd.get("https://usaco.org/index.php")

wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div[1]/div/form/div/div[2]/input').send_keys('jacobtrentini')
wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div[1]/div/form/div/div[3]/input').send_keys('d7f3132')
wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div[1]/div/form/div/div[5]/span/input').click()

def get_problem_grade(problem):
    print("Finding solution for problem: ", problem)
    try: 
        with open('/Users/jacobtrentini/Development/USACOWebcrawl/tempCode.py', 'w') as tempFile:
            code = problems[problem]['code']
            code = code[code.find('```')+3:code.rfind('```')]
            wd.get(problem)
            tempFile.write(code)

            # navigate to each usaco problem and submit the code through form and sendKeys

            wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[6]/form/div/div[1]/select/option[6]').click()
            wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[6]/form/div/div[2]/input').send_keys('/Users/jacobtrentini/Development/USACOWebcrawl/tempCode.py')
            wd.find_element(By.XPATH, '//*[@id="solution-submit"]').click()
            print("Solution submitted for problem: ", problem)
            exit(1)

    except Exception as e:
        print(f"Failed finding solution for {problem} with error: {e}")

for problem in problems:
    get_problem_grade(problem)
