import requests
import json

def get_departures():
    api_key = "YOUR_API_KEY"
    url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:41251:"
    headers = {'Accept': 'application/json','apikey': "vD5EOap2m5uSuMZmcYgh3pRbmsDlfQ3s"}
    response = requests.get(url, headers=headers)
    data = response.json()

    with open("departures.json", "w") as file:
        json.dump(data, file)

    # # Extraire et afficher les informations sur les départs surveillés
    # stop_monitoring = data['Siri']['ServiceDelivery']['StopMonitoringDelivery']
    # for stop in stop_monitoring:
    #     monitored_visits = stop['MonitoredStopVisit']
    #     for visit in monitored_visits:
    #         recorded_at_time = visit['RecordedAtTime']
    #         monitored_vehicle_journey = visit['MonitoredVehicleJourney']
    #         line_ref = monitored_vehicle_journey['LineRef']['value']
    #         direction_name = monitored_vehicle_journey['DirectionName'][0]['value']
    #         destination_ref = monitored_vehicle_journey['DestinationRef']['value']
    #         destination_name = monitored_vehicle_journey['DestinationName'][0]['value']
    #         expected_arrival_time = monitored_vehicle_journey['MonitoredCall']['ExpectedArrivalTime']
    #         expected_departure_time = monitored_vehicle_journey['MonitoredCall']['ExpectedDepartureTime']
    #         departure_status = monitored_vehicle_journey['MonitoredCall']['DepartureStatus']

    #         # Afficher les informations
    #         print(f"Line: {line_ref}, Direction: {direction_name}, Destination: {destination_name}")
    #         print(f"Expected Arrival: {expected_arrival_time}, Expected Departure: {expected_departure_time}")
    #         print(f"Departure Status: {departure_status}")
    #         print()

    return "Data saved to departures.json"

if __name__ == "__main__":
    print(get_departures())
