from netmiko import ConnectHandler
import requests

# Device info
device = {
    "device_type": "cisco_ios",
    "host": "192.168.206.10",
    "username": "praneeth",
    "password": "gns3pass",
    "secret": "gns3pass",
}

# Connect and get config
net_connect = ConnectHandler(**device)
net_connect.enable()
config = net_connect.send_command("show running-config")

# NetBox info
NETBOX_URL = "http://192.168.206.139:8000/api/"
NETBOX_TOKEN = "bfcfee365ff4f6f62201326e6c1a3e76e7c06ea3"
HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Get device ID from NetBox
hostname = net_connect.send_command("show run | include hostname").split()[1]
r = requests.get(f"{NETBOX_URL}dcim/devices/?name={hostname}", headers=HEADERS)
device_id = r.json()["results"][0]["id"]

# Update comment field with config
payload = {
    "comments": config[:65500]  # truncate if too large
}
r = requests.patch(f"{NETBOX_URL}dcim/devices/{device_id}/", headers=HEADERS, json=payload)

if r.status_code == 200:
    print(f"✅ Running-config pushed to NetBox comments for device '{hostname}'.")
else:
    print(f"❌ Failed to update comments: {r.status_code}")
    print(r.text)
