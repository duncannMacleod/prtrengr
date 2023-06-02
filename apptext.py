import requests
import json
import datetime
import pytz


def compare_times(time_str1):
    time_str1=convert_time(time_str1)
    time_str2=datetime.datetime.now().strftime("%H:%M")
    time_obj1 = datetime.datetime.strptime(time_str1, "%H:%M")
    time_obj2 = datetime.datetime.strptime(time_str2, "%H:%M")
    
    return time_obj1 > time_obj2


def get_current_time():
    tz = pytz.timezone('Europe/Paris')
    current_time = datetime.datetime.now(tz)
    return current_time


def convert_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time_obj.strftime("%H:%M")

def adjust_departure_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    time_obj = time_obj + datetime.timedelta(hours=2)  # Ajouter 2 heures
    return time_obj.strftime("%H:%M")

def get_departures():
    url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A41251%3A"
    headers = {'Accept': 'application/json', 'apikey': "vD5EOap2m5uSuMZmcYgh3pRbmsDlfQ3s"}
    response = requests.get(url, headers=headers)
    data = response.json()

    with open("departures.json", "w") as file:
        json.dump(data, file)

    process_departures(data, limit=5)  # Pass the limit as an argument

    return "Data saved to departures.json"

def process_departures(data, limit):
    stop_monitoring = data['Siri']['ServiceDelivery']['StopMonitoringDelivery']
    departures = []

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
                expected_departure_time = monitored_call.get('ExpectedDepartureTime', 'Unknown')
                vehicle_at_stop = monitored_call.get('VehicleAtStop', False)
            else:
                expected_departure_time = "2023-06-02T00:00:00.000Z"
                vehicle_at_stop = False

            if compare_times(expected_departure_time):
                departure = {
                    'line_ref': line_ref,
                    'expected_departure_time': expected_departure_time,
                'destination_name': destination_name
                }
                departures.append(departure)

    sorted_departures = sorted(departures, key=lambda d: d['expected_departure_time'])

    count = 0  # Initialize count variable
    for departure in sorted_departures:
        if count >= limit:
            break  # Exit the loop after reaching the limit
        line_ref = departure['line_ref']
        expected_departure_time = departure['expected_departure_time']
        destination_name = departure['destination_name']
        if line_ref == "STIF:Line::C01741:":
            print(f"Ligne U, Destination: {destination_name}, Expected Departure: {expected_departure_time}")
        if line_ref == "STIF:Line::C01736:":
            print(f"Ligne N, Destination: {destination_name}, Expected Departure: {expected_departure_time}")
        if line_ref == "STIF:Line::C01727:":
            print(f"Ligne C, Destination: {destination_name}, Expected Departure: {expected_departure_time}")
        print()
        count += 1  # Increment the count variable

    return "Data processed successfully"

if __name__ == "__main__":
    print(get_departures())