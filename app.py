from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/departures')
def get_departures():
    url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:463158:"
    headers = {
        'Authorization': 'Bearer VOTRE_CLÉ_API',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    departures = data['DepartureBoard']['Departure']

    return render_template('departures.html', departures=departures)

if __name__ == '__main__':
    app.run()
