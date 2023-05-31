function getDepartures() {
    var url = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:463158:";

    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        headers: {
            "Authorization": "Bearer " + apiKey
        },
        success: function(data) {
            var departures = data.Siri.ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit;

            for (var i = 0; i < departures.length; i++) {
                var departure = departures[i];
                var destination = departure.MonitoredVehicleJourney.DestinationName;
                var time = departure.MonitoredVehicleJourney.MonitoredCall.ExpectedDepartureTime;

                var horaireElement = $("<p>").text("Prochain départ pour " + destination + " : " + time);
                $("#horaires").append(horaireElement);
            }
        },
        error: function(xhr, status, error) {
            console.log("Une erreur s'est produite lors de la récupération des horaires :", error);
        }
    });
}
