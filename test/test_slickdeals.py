import logging

import pandas as pd

import slickdeals as sd

logging.basicConfig(level=logging.DEBUG)


def test_format_message():
    # arrange
    df = pd.DataFrame([{
        'original-price': 99,
        'store': 'amzn',
        'url': 'https://example.com'
    }])
    fetcher = sd.SlickDealsFetcher()
    # act
    msg = fetcher.format_message(df)
    logging.error(msg)
    assert 0
