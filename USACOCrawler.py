from bs4 import BeautifulSoup
import requests

class USACOCrawler:
    base_url = 'https://usaco.org'

    @staticmethod
    def get_contest_links() -> list:
        website_text = requests.get(f'{USACOCrawler.base_url}/index.php?page=contests').text
        soup = BeautifulSoup(website_text, 'html.parser')
        allResults = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=') and tag.get('href').endswith('results'))
        return [link.get('href') for link in allResults]

    @staticmethod
    def get_contest_problems(contest_link: str) -> list:
        website_text = requests.get(f'{USACOCrawler.base_url}/{contest_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        contest_problems = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=viewproblem2'))
        return [problem.get('href') for problem in contest_problems]

    @staticmethod
    def get_contest_problem(contest_problem_link: str) -> str:
        website_text = requests.get(f'{USACOCrawler.base_url}/{contest_problem_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        return USACOCrawler._clean_contest_problem(soup.find('div', {'class': 'problem-text'}).text)

    @staticmethod
    def _clean_contest_problem(contest_problem_text) -> str:
        contest_problem_text = contest_problem_text.replace('\leq', '<=') # preceeds 'le' on purpose
        contest_problem_text = contest_problem_text.replace('\geq', '>=')
        contest_problem_text = contest_problem_text.replace('\le', '<')
        contest_problem_text = contest_problem_text.replace('\ge', '>')
        contest_problem_text = contest_problem_text.replace('$', '')
        return contest_problem_text

class CSVHelper:
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name

    def write_to_csv(self, problem_text: str, problem_link: str):
        with open(self.file_name, 'a') as file:
            file.write(f'{problem_link},{problem_text}\n')

# Crawler Example Usage


contests = USACOCrawler.get_contest_links()
print(contests)
contest_problems = USACOCrawler.get_contest_problems(contests[0])
print(contest_problems[0])
problem = USACOCrawler.get_contest_problem(contest_problems[0])
print(problem)

# CSV Example Usage

CSVHelper("/Users/jacobtrentini/Development/USACOWebcrawl/usaco_problems.csv").write_to_csv(problem, contest_problems[0])
