import requests
import json
import datetime
import pytz
import os
import PySimpleGUI as sg
import time

layout=[]


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

def Station_Name(stop_point):
    with open("stations_names.json",'r') as f:
        data=json.load(f)
    station_list=data['Station_Names']
    for key in station_list:
        if key==stop_point:
            return station_list[key]
    return None

def get_departures(departures,stop_point):
    base_url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef={}"
    url= base_url.format(stop_point)
    headers = {'Accept': 'application/json', 'apikey': "vD5EOap2m5uSuMZmcYgh3pRbmsDlfQ3s"}
    response = requests.get(url, headers=headers)
    data = response.json()

    with open("departures.json", "w") as file:
        json.dump(data, file,indent=4)

    process_departures(data,departures)

    return "Data saved to departures.json"

def process_departures(data,departures):
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
            if expected_departure_time == "Unknown":
                expected_departure_time=monitored_call.get('ExpectedDepartureTime', 'Unknown')
            departure = {
                'line_ref': line_ref,
                'expected_departure_time': expected_departure_time,
                'destination_name': destination_name,
                'platform_name': platform_name
            }

            if departure not in displayed_departures and compare_times(expected_departure_time):  # Vérifier si le départ est déjà affiché
                departures.append(departure)
                displayed_departures.append(departure)  # Ajouter le départ à la liste des affichés

    #departures = sorted(departures, key=lambda d: d['expected_departure_time'])



def display_departures(limit,stop_point):
    global layout
    del layout[:]
    # Définir la mise en page de la fenêtre
    sation_name=Station_Name(stop_point)
    layout = [[sg.Text(f"Prochains départs en gare de {sation_name}", font=("Helvetica", 20)),
        sg.Button(key='Actualiser', image_filename ='actualiser.png', border_width=5),sg.Button(key='Fermer',image_filename='fermer.png', border_width=5)],]


    departures = []

    get_departures(departures,stop_point)

    # Définition des chemins vers les logos des lignes
    logo_u = 'logo_u.png'
    logo_n = 'logo_n.png'
    logo_c = 'logo_c.png'
    logo_a = 'logo_a.png'
    logo_b = 'logo_b.png'
    logo_d = 'logo_d.png'
    logo_ter = 'logo_ter.png'
    logo_l = 'logo_l.png'
    logo_j = 'logo_j.png'
  

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
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01736:":
            line_logo = logo_n
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01727:":
            line_logo = logo_c
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        
        elif line_ref == "STIF:Line::C01742:":
            line_logo = logo_a
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01743:":
            line_logo = logo_b
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01728:":
            line_logo = logo_d
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01740:": #ligne l
            line_logo = logo_l
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01739:": #ligne j
            line_logo = logo_j
            line_text = f" {destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01744:" or "STIF:Line::C02370:" or "STIF:Line::C02375:":#lignes ter
            line_logo = logo_ter
            line_text = f" {destination_name}, Départ prévu à: {convert_time_expected}"
        else:
            line_logo = None
            line_text = ""
        
        layout.append([sg.Image(line_logo, size=(32, 32),key=f'-IMAGE-{count}-'), sg.Text(line_text,key=f'-TEXT-{count}-',font=("Helvetica", 13))])
        count += 1
    return layout

    #window = sg.Window('Window Title', layout, no_titlebar=True, location=(0,0), size=(1366,768), keep_on_top=True)









def setup_layout(limit,stop_point):
    sation_name=Station_Name(stop_point)
    layout = [[sg.Text(f"Prochains départs en gare de {sation_name}", font=("Helvetica", 20)),
        sg.Button(key='Actualiser', image_filename ='actualiser.png', border_width=5),sg.Button(key='Fermer',image_filename='fermer.png', border_width=5)],]

    for i in range(limit)-1:
        layout.append([sg.Image(key=f'-IMAGE-{i}-'), sg.Text(key=f'-TEXT-{i}-', font=("Helvetica", 13))])

    return layout
    
def actualize_departures(limit,stop_point):
    departure_list=[]
    departures = []

    get_departures(departures,stop_point)

    # Définition des chemins vers les logos des lignes
    logo_u = 'logo_u.png'
    logo_n = 'logo_n.png'
    logo_c = 'logo_c.png'
    logo_a = 'logo_a.png'
    logo_b = 'logo_b.png'
    logo_d = 'logo_d.png'
    logo_ter = 'logo_ter.png'
    logo_l = 'logo_l.png'
    logo_j = 'logo_j.png'
  

    count = 1
    
    for departure in departures:
        if count >= limit+1:
            break
        
        line_ref = departure['line_ref']
        expected_departure_time = departure['expected_departure_time']
        destination_name = departure['destination_name']
        convert_time_expected = convert_time(expected_departure_time)
        
        if line_ref == "STIF:Line::C01741:":
            line_logo = logo_u
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01736:":
            line_logo = logo_n
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01727:":
            line_logo = logo_c
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01742:":
            line_logo = logo_a
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01743:":
            line_logo = logo_b
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01728:":
            line_logo = logo_d
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01740:": #ligne l
            line_logo = logo_l
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01739:": #ligne j
            line_logo = logo_j
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        elif line_ref == "STIF:Line::C01744:" or "STIF:Line::C02370:" or "STIF:Line::C02375:": #ligne ter
            line_logo = logo_ter
            line_text = f"{destination_name}, Départ prévu à: {convert_time_expected}"
        else:
            line_logo = None
            line_text = ""
        
        departure_list.append((line_logo, line_text))
        count += 1

    return departure_list
    

def main():
    global layout
    limit=5
    stop_point='STIF%3AStopPoint%3AQ%3A41251%3A'
    layout=display_departures(limit,stop_point)
    
    window = sg.Window('Prochains départs', layout,no_titlebar=False,keep_on_top=False,location=(0,15))
    # departure_list=actualize_departures(limit,stop_point)#modifie la variable globale layout
    # for i, (line_logo, line_text) in enumerate(departure_list):
    #         window.refresh()
    #         window[f'-IMAGE-{i}-'].update(filename=line_logo)
    #         window[f'-TEXT-{i}-'].update(line_text)
            

    
    last_update_minute = datetime.datetime.now().minute
    while True:
        event, values = window.read(timeout=5000)
        if event == sg.WINDOW_CLOSED or event == "Fermer":
            break
        current_minute = datetime.datetime.now().minute
        if event == "Actualiser"or current_minute != last_update_minute:
            # Récupérer les nouveaux départs
            departure_list=[]
            departure_list = actualize_departures(limit,stop_point)  # Récupérer les nouveaux départs (à remplacer par votre code)

            for i, (line_logo, line_text) in enumerate(departure_list):
                window.refresh()
                window[f'-IMAGE-{i}-'].update(filename=line_logo)
                window[f'-TEXT-{i}-'].update(line_text)
            
            last_update_minute = current_minute

    window.close()

if __name__ == "__main__":
    main()