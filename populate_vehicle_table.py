import boto3

def populate_vehicle_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VehicleTable-Otuoma-Caroline-s2110913')
    
    # List of dummy number plates
    dummy_plates = [
        {"VehicleId": "6777 NP 17", "status": "Whitelisted"},
        {"VehicleId": "6778 NP 18", "status": "Whitelisted"},
        {"VehicleId": "6779 NP 19", "status": "Whitelisted"},
        {"VehicleId": "6780 NP 20", "status": "Whitelisted"},
        {"VehicleId": "6781 NP 21", "status": "Whitelisted"},
        {"VehicleId": "6782 NP 22", "status": "Whitelisted"},
        {"VehicleId": "6783 NP 23", "status": "Whitelisted"},
        {"VehicleId": "6784 NP 24", "status": "Whitelisted"},
        {"VehicleId": "6785 NP 25", "status": "Whitelisted"},
        {"VehicleId": "6786 NP 26", "status": "Whitelisted"},
        {"VehicleId": "6585 OC 11", "status": "Blacklisted"},
        {"VehicleId": "10652 OC 22", "status": "Blacklisted"}
    ]
    
    for plate in dummy_plates:
        table.put_item(Item=plate)
    
    print("Dummy data inserted into the table.")

if __name__ == "__main__":
    populate_vehicle_table()
