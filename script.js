document.addEventListener("DOMContentLoaded", function() {
    var url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:463158:";
    var horairesDiv = document.getElementById("horaires");

    fetch(url)
        .then(response => response.json())
        .then(data => {
            var departures = data.Siri.ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit;
            
            departures.forEach(departure => {
                var destination = departure.MonitoredVehicleJourney.DestinationName;
                var time = departure.MonitoredVehicleJourney.MonitoredCall.ExpectedDepartureTime;

                var horaireElement = document.createElement("p");
                horaireElement.textContent = "Prochain départ pour " + destination + " : " + time;
                horairesDiv.appendChild(horaireElement);
            });
        })
        .catch(error => {
            console.log("Une erreur s'est produite lors de la récupération des horaires :", error);
        });
});
