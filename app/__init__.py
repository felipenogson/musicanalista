from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from config import Config
from helpers import df, get_musicbrainz_info, get_my_year_album
import wikipedia

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

@app.route('/')
def index():
	list_of_years = df['Release Date'].unique().tolist()
	list_of_years.sort(reverse=True)
	return render_template('index.html', years=list_of_years)

@app.route('/results', methods=['POST'])
def results():
	if request.method == "POST":
		year = request.form['year']
		year_album = get_my_year_album(int(year))
		album_info = get_musicbrainz_info(year_album)
		try:
			wiki = wikipedia.page(f"{album_info['Album']} {album_info['Artist Name']} {album_info['Release Date']}")
		except: 
			wiki = ''
		return render_template('results.html', album_info=album_info, wiki=wiki)
	return "404"
	# return render_template('results.html')