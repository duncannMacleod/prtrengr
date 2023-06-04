import requests
import json
import datetime
import pytz
import os
import PySimpleGUI as sg
import time
def main():
    display_departures(limit=4)

def compare_times(time_str1):
    time_str1 = convert_time(time_str1)
    
    if time_str1 != "Unknown":
        time_str2 = datetime.datetime.now().strftime("%H:%M")
        time_obj1 = datetime.datetime.strptime(time_str1, "%H:%M")
        time_obj2 = datetime.datetime.strptime(time_str2, "%H:%M")
        
        return time_obj1 > time_obj2
    else:
        return False


def get_current_time():
    tz = pytz.timezone('Europe/Paris')
    current_time = datetime.datetime.now(tz)
    return current_time


def convert_time(time_str):
    if time_str != "Unknown":
        time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        time_obj = time_obj + datetime.timedelta(hours=2)  # Ajouter 2 heures
        return time_obj.strftime("%H:%M")
    else:
        return "Unknown"

def adjust_departure_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    time_obj = time_obj + datetime.timedelta(hours=2)  # Ajouter 2 heures
    return time_obj.strftime("%H:%M")

def get_departures(departures):
    url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A41251%3A"
    headers = {'Accept': 'application/json', 'apikey': "vD5EOap2m5uSuMZmcYgh3pRbmsDlfQ3s"}
    response = requests.get(url, headers=headers)
    data = response.json()

    with open("departures.json", "w") as file:
        json.dump(data, file,indent=4)

    process_departures(data,departures,limit=4)  # Pass the limit as an argument

    return "Data saved to departures.json"

def process_departures(data,departures,limit):
    stop_monitoring = data['Siri']['ServiceDelivery']['StopMonitoringDelivery']
    
    displayed_departures = []  # Liste pour stocker les départs déjà affichés

    for stop in stop_monitoring:
        monitored_visits = stop['MonitoredStopVisit']
        for visit in monitored_visits:
            recorded_at_time = visit['RecordedAtTime']
            monitored_vehicle_journey = visit['MonitoredVehicleJourney']
            line_ref = monitored_vehicle_journey['LineRef']['value']
            
            if 'DirectionName' in monitored_vehicle_journey and monitored_vehicle_journey['DirectionName']:
                direction_name = monitored_vehicle_journey['DirectionName'][0]['value']
            else:
                direction_name = "Unknown"
            destination_ref = monitored_vehicle_journey['DestinationRef']['value']
            destination_name = monitored_vehicle_journey['DestinationName'][0]['value']
            

            if 'MonitoredCall' in monitored_vehicle_journey:
                monitored_call = monitored_vehicle_journey['MonitoredCall']
                expected_departure_time = monitored_call.get('AimedDepartureTime', 'Unknown')
                vehicle_at_stop = monitored_call.get('VehicleAtStop', False)
                platform_name = monitored_call.get('ArrivalPlatformName', {}).get('value', 'Unknown')
            else:
                expected_departure_time = "2023-01-01T00:00:00.000Z"
                vehicle_at_stop = False

            departure = {
                'line_ref': line_ref,
                'expected_departure_time': expected_departure_time,
                'destination_name': destination_name,
                'platform_name': platform_name
            }

            if departure not in displayed_departures and compare_times(expected_departure_time):  # Vérifier si le départ est déjà affiché
                departures.append(departure)
                displayed_departures.append(departure)  # Ajouter le départ à la liste des affichés

    departures = sorted(departures, key=lambda d: d['expected_departure_time'])
    #display_departures(departures, limit)


def display_departures(limit):
    # Définir la mise en page de la fenêtre
    layout = [
        [sg.Text("Prochains départs", font=("Helvetica", 16))],
        [sg.Button("Actualiser")],
    ]

    departures = []

    get_departures(departures)

    # Définition des chemins vers les logos des lignes
    logo_u = 'logo_u.png'
    logo_n = 'logo_n.png'
    logo_c = 'logo_c.png'

    def update_departures():
        global departures
        departures = get_departures(limit)

    def refresh_window(window):
        window.refresh()

    count = 0
    for departure in departures:
        if count >= limit:
            break
        
        line_ref = departure['line_ref']
        expected_departure_time = departure['expected_departure_time']
        destination_name = departure['destination_name']
        convert_time_expected = convert_time(expected_departure_time)
        
        if line_ref == "STIF:Line::C01741:":
            line_logo = logo_u
            line_text = f"Destination: {destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01736:":
            line_logo = logo_n
            line_text = f"Destination: {destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01727:":
            line_logo = logo_c
            line_text = f"Destination: {destination_name}, Départ prévu à: {convert_time_expected}"
        else:
            line_logo = None
            line_text = ""
        
        layout.append([sg.Image(line_logo, size=(32, 32)), sg.Text(line_text)])
        count += 1

    window = sg.Window('Prochains départs', layout)

    # Boucle principale
    while True:
        event, values = window.read(timeout=60000)  # Actualisation toutes les 60 secondes
        if event == sg.WINDOW_CLOSED or event == "Quitter":
            break
        elif event == "Actualiser":
            update_departures()
            refresh_window(window)

    # Fermer la fenêtre et terminer le programme
    window.close()






if __name__ == "__main__":
    main()
