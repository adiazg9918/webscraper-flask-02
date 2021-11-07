from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from classScraper import Scraper

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    request_method = request.method
    if request_method == "POST":
        user = request.form['name']
        return redirect(url_for('results', user=user))
    return render_template('index.html', request_method=request_method)


@app.route('/results/<string:user>')
def results(user):
    ni = str(user)
    scraper = Scraper(ni)
    scraper.get_url()
    scraper.navigate()
    scraper.get_data()
    scraper.to_csv()

    return render_template('results.html', proxies=scraper.records)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
