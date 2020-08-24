import requests
from bs4 import BeautifulSoup
import unicodedata
import json
from flask import Flask, Response

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return Response("<h1>Flask</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")

# "img" https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_UY512.jpg
def convert_query(query):
	nfkd_form = unicodedata.normalize('NFKD', query)
	only_ascii = nfkd_form.encode('ascii', 'ignore').lower().decode('ascii')
	final_query = ''
	for c in only_ascii:
		if c == ' ':
			final_query+='_'
		elif (ord(c)>=97 and ord(c)<=122) or c =='_':
			final_query+=c
	return final_query

def do_scrap(query):
	query = convert_query(query)
	if len(query) == 0:
		return []
	url = "https://v2.sg.media-imdb.com/suggestion/{}/{}.json".format(query[0], query)
	response = requests.get(url).text
	movies =  json.loads(response).get("d")
	if not movies:
		return []
	keys = ["i", "id", "l", "q", "rank", "s", "vt", "y"]
	movies_parsed = []
	for d in movies:
		movies_parsed.append({ k : d.get(k) for k in keys})
	return movies_parsed

if __name__ == "__main__":
	print(do_scrap("avengers"))