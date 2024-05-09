from bs4 import BeautifulSoup
import requests

class USACOParser:
    base_url = 'https://usaco.org'

    @staticmethod
    def get_contest_links() -> list:
        website_text = requests.get(f'{USACOParser.base_url}/index.php?page=contests').text
        soup = BeautifulSoup(website_text, 'html.parser')
        allResults = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=') and tag.get('href').endswith('results'))
        return [link.get('href') for link in allResults]

    @staticmethod
    def get_contest_problems(contest_link: str) -> list:
        website_text = requests.get(f'{USACOParser.base_url}/{contest_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        contest_problems = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href').startswith('index.php?page=viewproblem2'))
        return [problem.get('href') for problem in contest_problems]

    @staticmethod
    def get_contest_problem(contest_problem_link: str) -> str:
        website_text = requests.get(f'{USACOParser.base_url}/{contest_problem_link}').text
        soup = BeautifulSoup(website_text, 'html.parser')
        return soup.find('div', {'class': 'problem-text'}).text

contests = USACOParser.get_contest_links()
print(contests)
contest_problems = USACOParser.get_contest_problems(contests[0])
print(contest_problems)
problem = USACOParser.get_contest_problem(contest_problems[0])
print(problem)
