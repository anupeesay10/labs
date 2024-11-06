from flask import Flask, render_template, request
from datetime import datetime
import apod_model  # Import the model

app = Flask(__name__)

@app.route('/')
def home():
    """Landing Page displaying today's APOD."""
    apod_data = apod_model.get_apod()
    return render_template('home.html', apod=apod_data)

@app.route('/history', methods=['GET', 'POST'])
def history():
    """History Page allowing users to view APODs by date."""
    apod_data = None
    max_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
    if request.method == 'POST':
        date = request.form['date']
        if date:
            apod_data = apod_model.get_apod(date)
    return render_template('history.html', apod=apod_data, max_date=max_date)

if __name__ == '__main__':
    app.run(debug=True)