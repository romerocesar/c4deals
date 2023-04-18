import logging

import discord
import yaml

from slickdeals import SlickDealsFetcher

logging.basicConfig(level=logging.DEBUG)


class C4Deals(discord.Client):

    def __init__(self, *args, config=None, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(*args, intents=intents, **kwargs)
        self.approvers = config.get('approvers')
        self.token = config.get('token')
        self.deals_fetcher = SlickDealsFetcher(html=open('test.html').read())

    async def on_ready(self):
        deals = self.deals_fetcher.fetch_deals()
        for userid in self.approvers:
            user = await client.fetch_user(userid)
            deal = deals.iloc[0]
            msg = self.deals_fetcher.format_message(deal)
            await user.send(msg)


config = yaml.safe_load(open('config.yaml'))
client = C4Deals(config=config)

client.run(config.get('token'))
