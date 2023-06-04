import requests
import json
import datetime
import pytz
import os
import PySimpleGUI as sg
import time

departures = []
window = None
layout=[]
def main():
    display_departures(limit=10,stop_point='STIF%3AStopPoint%3AQ%3A41207%3A')



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

<<<<<<< HEAD:app.py
def Station_Name(stop_point):
    with open("stations_names.json",'r') as f:
        data=json.load(f)
    station_list=data['Station_Names']
    for key in station_list:
        if key==stop_point:
            return station_list[key]
    return None

def get_departures(stop_point):
    base_url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef={}"
    url= base_url.format(stop_point)
=======
def get_departures(departures):
    url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A41251%3A"
>>>>>>> parent of ae441a9 (.):apptext.py
    headers = {'Accept': 'application/json', 'apikey': "vD5EOap2m5uSuMZmcYgh3pRbmsDlfQ3s"}
    response = requests.get(url, headers=headers)
    data = response.json()

    with open("departures.json", "w") as file:
        json.dump(data, file,indent=4)

<<<<<<< HEAD:app.py
    process_departures(data)
=======
    process_departures(data,departures)  # Pass the limit as an argument
>>>>>>> parent of ae441a9 (.):apptext.py

    return "Data saved to departures.json"

def process_departures(data):
    global departures
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

<<<<<<< HEAD:app.py
def refresh_window(window):
        window.refresh()
def update_departures(stop_point,limit):
    global departures
    
    # Définir la mise en page de la fenêtre
    station_name=Station_Name(stop_point)
    global layout

    layout = [
        [sg.Text(f"Prochains départs en gare de {station_name}", font=("Helvetica", 16)),sg.Button("Actualiser")],
    ]

    get_departures(stop_point)
=======

def display_departures(limit):
    # Définir la mise en page de la fenêtre
    layout = [
        [sg.Text("Prochains départs", font=("Helvetica", 16))],
        [sg.Button("Actualiser")],
    ]

    departures = []

    get_departures(departures)
>>>>>>> parent of ae441a9 (.):apptext.py

    # Définition des chemins vers les logos des lignes
    logo_u = 'logo_u.png'
    logo_n = 'logo_n.png'
    logo_c = 'logo_c.png'
<<<<<<< HEAD:app.py
    logo_ter = 'logo_ter.png' 
=======

    def update_departures(departures,limit):
        departures = get_departures(limit)

    def refresh_window(window):
        window.refresh()
>>>>>>> parent of ae441a9 (.):apptext.py

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

    
def display_departures(limit,stop_point):
    
    global departures
    global window
    global layout
    layout = [[sg.Text("x")]]
    window= sg.Window('Prochains départs',layout)
    # Boucle principale
    while True:
<<<<<<< HEAD:app.py
        update_departures(stop_point,limit)
        
        
        event, _ = window.read(timeout=10000)
        if event == sg.WINDOW_CLOSED or event == "Quitter":
            break
    window.close()


=======
        event, values = window.read(timeout=60000)  # Actualisation toutes les 60 secondes
        if event == sg.WINDOW_CLOSED or event == "Quitter":
            break
        elif event == "Actualiser":
            update_departures(departures,limit)
            refresh_window(window)

    # Fermer la fenêtre et terminer le programme
    window.close()



def main():
    display_departures(limit=4)

>>>>>>> parent of ae441a9 (.):apptext.py
if __name__ == "__main__":
    main()
