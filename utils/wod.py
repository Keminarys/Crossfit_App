import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random

def generate_random_crossfit_url() -> str:
    start = datetime.strptime("2001-10-02", "%Y-%m-%d")
    end = datetime.now()
    rand_day = random.randrange((end - start).days)
    rand_date = start + timedelta(days=rand_day)
    return f"https://www.crossfit.com/workout/{rand_date.strftime('%Y/%m/%d')}#/comments"

def fetch_hero_wods(url: str = "https://www.crossfit.com/heroes") -> list:
    response = requests.get(url)
    wods = []
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        sections = soup.find_all('section', class_='_component_1ugao_79')
        for section in sections:
            h3 = section.find('hr').find_next('h3')
            if h3:
                wod_name = h3.text.strip()
                wod_description = ''
                for sib in h3.find_next_siblings():
                    if sib.name == 'p':
                        wod_description += sib.get_text(separator="\n", strip=True) + '\n\n'
                    else:
                        break
                wods.append({"name": wod_name, "description": wod_description.strip()})
    return wods
