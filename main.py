import requests
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime

import settings
from twilio.rest import Client


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def test_parse_html():
    with open('ue.html') as html:
        soup = parse_html(html)
        assert soup.title.string.index("Unemployment") != -1


def search_for_ss_number(soup, ss_number):
    days = soup.select('.accordion > .card')
    for day in days:
        slots = day.find_all('td')
        for slot in slots:
            container = slot.find('span')
            if container:
                items = container.text.strip()
                normalized_items = unicodedata.normalize("NFKD", items)
                if normalized_items.startswith("M") or normalized_items.startswith("F"):
                    # Limitation of UE website. There's instructions written in some
                    # spans and there's no easy way to filter from classes/ids
                    continue
                else:
                    split_items = normalized_items.split("  ")
                    if len(split_items) != 3:
                        # Another limitation of UE website. One instance of a span that returned an array
                        # With a single empty string
                        continue
                    start_range = split_items[0]
                    end_range = split_items[1]
                    time = split_items[2]
                    # Check to see if the last four of the social matches a span
                    # If so, break the search and return day_string and time
                    found = int(start_range) <= ss_number and ss_number <= int(end_range)
                    if found:
                        day_string = day.find('button').text.strip().split(":")[0]
                        return (day_string, time)
    return (-1, -1)

def get_ue_html(url):
    resp = requests.get(url)
    return resp.text


def get_week(soup):
    return soup.title.string.split("|")[1].split(":")[0]


if __name__ == "__main__":
    url = "https://myunemployment.nj.gov/labor/myunemployment/schedule.shtml"
    html = get_ue_html(url="https://myunemployment.nj.gov/labor/myunemployment/schedule.shtml")
    soup = parse_html(html=html)
    week = get_week(soup=soup)
    (day, time) = search_for_ss_number(soup, settings.UE_SEARCH_SS)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    body = f"\n{week}\n{day} between {time}"
    if day == -1 or time == -1:
        body = f"Could not find timeslot. Please check {url}"

    message = client.messages.create(
        body=body,
        to=settings.TWILIO_TO_NUMBER,
        from_=settings.TWILIO_FROM_NUMBER
    )
    print(message)
