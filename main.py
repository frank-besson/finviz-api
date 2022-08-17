import os, json
import psutil
from cachetools import TTLCache
from finviz import get_stock, get_insider, get_news, get_analyst_price_targets
import requests
from flask import Flask

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

get_stock_cache = TTLCache(maxsize=100, ttl=60*15)
get_insider_cache = TTLCache(maxsize=100, ttl=60*15)
get_news_cache = TTLCache(maxsize=100, ttl=60*15)
get_analyst_price_targets_cache = TTLCache(maxsize=100, ttl=60*15)

app = Flask(__name__)
 
# https://www.section.io/engineering-education/implementing-rate-limiting-in-flask/
limiter = Limiter(app, key_func=get_remote_address)

def get_from_cache(key, cache, get_func):
	'''
	Try to fetch value of key from cache
	If not value found, execute get_func to find value that should be cached
	
	Parameters:
	key (str): keyname that should exist/will exist in cache
	cache (cachetools.TTLCache): instance of TTLCache that should be queryed
	get_func (callable func): function that should be executed if key&val not in cache
	
	Returns:
	contents of cache at key
	'''
	
	try:
		return cache[key]
	except KeyError:
		pass

	try:
		cache[key] = json.dumps(get_func(key))
		
		return cache[key]
	except requests.exceptions.HTTPError: # 404 error
		return json.dumps({'response':'not found'}), 404
	except Exception as e:
		return json.dumps({'response': str(e)}), 500
		

@app.route("/get_analyst_price_targets/<string:ticker>",  methods=['GET'])
@limiter.limit("5/hour")
def route_get_analyst_price_targets(ticker):
	return get_from_cache(ticker, get_analyst_price_targets_cache, get_analyst_price_targets)


@app.route("/get_news/<string:ticker>",  methods=['GET'])
@limiter.limit("5/hour")
def route_get_news(ticker):
	return get_from_cache(ticker, get_news_cache, get_news)

@limiter.limit("10/hour") # maximum of 10 requests per minute
@app.route("/get_insider/<string:ticker>",  methods=['GET'])
def route_get_insider(ticker):
	return get_from_cache(ticker, get_insider_cache, get_insider)


@app.route("/get_stock/<string:ticker>",  methods=['GET'])
@limiter.limit("5/hour")
def route_get_stock(ticker):
	return get_from_cache(ticker, get_stock_cache, get_stock)


@app.route("/util",  methods=['GET'])
@limiter.limit("5/hour")
def route_util():
	return json.dumps(psutil.virtual_memory())

@app.errorhandler(404)
def route_missing(err):
	return 'For routes and demo, please see https://github.com/frank-besson/finviz-api'

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 33507)), debug=False)