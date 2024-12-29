import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2

url = "https://nextrip-public-api.azure-api.net/octranspo/gtfs-rt-vp/beta/v1/VehiclePositions"
headers = {
    "Ocp-Apim-Subscription-Key": "",
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open("vehicle_positions.pb", "wb") as file:
        file.write(response.content)
    print("Vehicle positions data saved to vehicle_positions.pb")
else:
    print(f"Error: {response.status_code}, {response.text}")

feed = gtfs_realtime_pb2.FeedMessage()
with open("vehicle_positions.pb", "rb") as file:
    feed.ParseFromString(file.read())
for entity in feed.entity:
    if entity.HasField("vehicle"):
        vehicle = entity.vehicle
        print(f"Vehicle ID: {vehicle.vehicle.id}")
        print(f"Latitude: {round(vehicle.position.latitude,6)}")
        print(f"Longitude: {round(vehicle.position.longitude,6)}")
        print(f"Speed: {round(vehicle.position.speed*3.6,2)} km/h")
        print(f"Timestamp: {datetime.fromtimestamp(vehicle.timestamp)}")
        print()