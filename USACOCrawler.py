from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://usaco.org'
class USACOCrawler:

    @staticmethod
    def get_contest_links() -> list:
        print("Getting contest links")
        website_text = requests.get(f'{base_url}/index.php?page=contests').text
        soup = BeautifulSoup(website_text, 'html.parser')
        allResults = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=') and tag.get('href').endswith('results'))
        return [link.get('href') for link in allResults]

    @staticmethod
    def get_contest_problems(contest_link: str) -> list:
        print(f"========= Getting contest problems for {contest_link} ==========")
        website_text = requests.get(f'{base_url}/{contest_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        contest_problems = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=viewproblem2'))
        return [problem.get('href') for problem in contest_problems]

    @staticmethod
    def get_contest_problem(contest_problem_link: str) -> str:
        print(f"Getting contest problem for {contest_problem_link}")
        website_text = requests.get(f'{base_url}/{contest_problem_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        return USACOCrawler._clean_contest_problem(soup.find('div', {'class': 'problem-text'}).text)

    @staticmethod
    def _clean_contest_problem(contest_problem_text) -> str:
        contest_problem_text = contest_problem_text.replace('\leq', '<=') # preceeds 'le' on purpose
        contest_problem_text = contest_problem_text.replace('\geq', '>=')
        contest_problem_text = contest_problem_text.replace('\le', '<')
        contest_problem_text = contest_problem_text.replace('\ge', '>')
        contest_problem_text = contest_problem_text.replace('$', '')
        contest_problem_text = contest_problem_text.replace(',', '')
        contest_problem_text = contest_problem_text.replace('\n', ' ')
        return contest_problem_text

class FileHelper:
    file_name: str
    file_contents: dict = {} # memory buffer of file content, updated privately

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_contents = self._read_problems()

    def append_problem_to_file(self, problem_text: str, problem_link: str):
        with open(self.file_name, 'w') as file:
            self.file_contents[problem_link] = problem_text
            file.write(json.dumps(self.file_contents))
            print(f"Successfully wrote {problem_link}")

    def _read_problems(self) -> dict:
        with open(self.file_name, 'r') as file:
            return json.loads(file.read()) or {}

helper = FileHelper("/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems.json")

# Example Usage: Crawl all years with problems (2015 <-- 2024) and save to file
for contest in USACOCrawler.get_contest_links():
    for problem_link in USACOCrawler.get_contest_problems(contest):
        problem = USACOCrawler.get_contest_problem(problem_link)
        helper.append_problem_to_file(problem, problem_link)

print("Finished crawling USACO problems")
print("Total unique problems: ", len(helper.file_contents))


# Crawler Example Usage
"""
contests = USACOCrawler.get_contest_links()
#print(contests)
contest_problems = USACOCrawler.get_contest_problems(contests[0])
#print(contest_problems[0])
problem = USACOCrawler.get_contest_problem(contest_problems[0])
problem_two = USACOCrawler.get_contest_problem(contest_problems[1])
#print(problem)

# CSV Example Usage
fileHelper = FileHelper("/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems.json")
#fileHelper.append_problem_to_file(problem, contest_problems[0])
#fileHelper.append_problem_to_file(problem_two, contest_problems[1])
#FileHelper("/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems.json").append_problem_to_file(problem, contest_problems[0])
"""
