from datetime import datetime
import logging

from bs4 import BeautifulSoup
import pandas as pd
import requests
from tabulate import tabulate

logger = logging.getLogger('c4deals')
logging.basicConfig(level=logging.DEBUG)


class SlickDealsFetcher:

    def __init__(self, html=None, category='video-game-deals'):
        self.category = category
        self.base_url = 'https://slickdeals.net'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.html = html

    def fetch_deals(self):
        if self.html:
            decoded = self.html
        else:
            url = f"{self.base_url}/{self.category}/"
            response = requests.get(url, headers=self.headers)
            decoded = response.content.decode("utf-8")
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%s")
            fname = f'{now}.html'
            with open(fname, 'w') as fp:
                fp.write(decoded)
                logger.debug(f'wrote deals html into {fname=}')
        soup = BeautifulSoup(decoded, "html.parser")
        cards = soup.find_all("li", attrs={'data-catalogitem': "DealCard"})
        deals = []
        for card in cards:
            try:
                deals.append(self.parse_card(card))
            except Exception as e:
                logger.warning(f'failed to parse {card=}. {e}')
        df = pd.DataFrame(deals)
        return df

    def parse_card(self, card):
        deal = dict()
        deal['id'] = card.get('id')
        deal['title'] = card.find('a', class_="bp-c-card_title").text
        deal['price'] = card.find('span', class_="bp-p-dealCard_price").text
        if original := card.find('span', class_='bp-p-dealCard_originalPrice'):
            deal['original-price'] = original.text
        deal['fire'] = bool(card.find('span', class_='bp-i-bbFire'))
        deal['store'] = card.find('span', class_='bp-c-card_subtitle').text
        deal['votes'] = card.find('span', class_='bp-p-votingThumbsPopup_voteCount').text
        deal['frontpage'] = bool(card.find('span', class_='bp-c-label--frontpage'))
        deal['popular'] = bool(card.find('span', class_='bp-c-label--popular'))
        deal['url'] = f'{self.base_url}' + card.find('a', class_='bp-c-card_title').get('href')
        return deal

    def format_message(self, deal: pd.Series = None) -> str:
        return ' '.join(list(deal[['original-price', 'store', 'url']]))
