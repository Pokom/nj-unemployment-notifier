import requests
import unicodedata
from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def test_parse_html():
    with open('ue.html') as html:
        soup = parse_html(html)
        assert soup.title.string.index("Unemployment") != -1

def search_for_ss_number(soup, ss_number):
    # Find days containers
    # Iterate of days, finding timeslots for range of social security numbers
    # If the passed in number is in a given range, return the day and time
    days = soup.select('.accordion > .card')
    for day in days:
        slots = day.find_all('td')
        for slot in slots:
            container = slot.find('span')
            if container:
                items = container.text.strip()
                normalized_items = unicodedata.normalize("NFKD", items)
                if normalized_items.startswith("M") or normalized_items.startswith("F"):
                    continue
                else:
                    split_items = normalized_items.split("  ")
                    if len(split_items) != 3:
                        continue
                    start_range = split_items[0]
                    end_range = split_items[1]
                    time = split_items[2]
                    found = int(start_range) <= ss_number and ss_number <= int(end_range)
                    if found:
                        day_string = day.find('button').text.strip().split(":")[0]
                        return (day_string, time)
    return (-1, -1)


def test_search_for_ss_number():
    with open('schedule.shtml') as html:
        soup = parse_html(html)
        (day, time) = search_for_ss_number(soup, 7332)
        assert day == 0

def get_ue_html(url):
    resp = requests.get(url)
    return resp.text

if __name__ == "__main__":
    html = get_ue_html(url="https://myunemployment.nj.gov/labor/myunemployment/schedule.shtml")
    soup = parse_html(html=html)
    (day, time) = search_for_ss_number(soup, 1)

    print(day, time)