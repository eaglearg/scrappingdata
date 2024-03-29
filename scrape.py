import requests
import sys
from bs4 import BeautifulSoup

def get_pages_hn(total_pages):
    links = []
    subtext = []
    for i in range(1, total_pages+1):
        res = requests.get('https://news.ycombinator.com/news?p=' + str(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        links += soup.select('.storylink')
        subtext += soup.select('.subtext')
    return create_custom_hn(links, subtext)

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points })    
    return sort_stories_by_votes(hn)

if __name__ == '__main__':
    try:
        if int(sys.argv[1]):
            print(get_pages_hn(int(sys.argv[1])))
    except (IndexError, ValueError) as err:
        while True:
            try:
                pages_to_scrap = int(input("how many pages do you want to scrape? "))
                if pages_to_scrap > 0:
                    print(get_pages_hn(pages_to_scrap))
                    break
                else:
                    print("you must enter a number greater than 0")
            except ValueError as err:
                print("you must enter a number greater than 0")