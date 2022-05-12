# [finviz-api]( https://wavecakes-finviz.herokuapp.com/ )
Flask web application that utilizes a [TTL Cache](https://cachetools.readthedocs.io/en/stable/) and [The Unofficial Finviz API](https://github.com/mariostoev/finviz) (with some [minor tweaks](https://github.com/frank-besson/finviz)) to provide API access to [Finviz.com](https://finviz.com/)

## API Routes
### [get_stocks/\<str:ticker\>](https://wavecakes-finviz.herokuapp.com/get_stock/goog)
    Returns a dictionary containing stock data.
    :param ticker: stock symbol
    :type ticker: str
    :return dict
### [get_insider/\<str:ticker\>](https://wavecakes-finviz.herokuapp.com/get_insider/goog)
    Returns a list of dictionaries containing all recent insider transactions.
    :param ticker: stock symbol
    :return: list
### [get_news/\<str:ticker\>](https://wavecakes-finviz.herokuapp.com/get_news/goog)
    Returns a list of sets containing news headline and url
    :param ticker: stock symbol
    :return: list
### [get_analyst_price_targets/\<str:ticker\>](https://wavecakes-finviz.herokuapp.com/get_analyst_price_targets/goog)
    Returns a list of dictionaries containing all analyst ratings and Price targets
     - if any of 'price_from' or 'price_to' are not available in the DATA, then those values are set to default 0
    :param ticker: stock symbol
    :param last_ratings: most recent ratings to pull
    :return: list
