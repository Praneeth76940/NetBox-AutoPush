import requests
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException, NetmikoTimeoutException

# Device credentials
device = {
    "device_type": "cisco_ios",
    "host": "192.168.206.10",
    "username": "praneeth",
    "password": "gns3pass",
    "secret": "gns3pass",
}

# NetBox API details
NETBOX_URL = "http://192.168.206.139:8000/api/"
NETBOX_TOKEN = "bfcfee365ff4f6f62201326e6c1a3e76e7c06ea3"
HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

try:
    print(f"🔌 Connecting to device {device['host']}...")
    net_connect = ConnectHandler(**device)
    net_connect.enable()

    hostname_line = net_connect.send_command("show run | include hostname")
    hostname = hostname_line.split()[1] if hostname_line else "Unknown"
    mgmt_ip = device["host"]
    print(f"📡 Retrieved hostname: {hostname}")

    # Payload
    device_payload = {
        "name": hostname,
        "device_type": 1,
        "device_role": 1,
        "site": 1,
        "status": "active",
    }

    print("📤 Pushing device to NetBox...")
    response = requests.post(f"{NETBOX_URL}dcim/devices/", headers=HEADERS, json=device_payload)

    if response.status_code == 201:
        print(f"✅ Device '{hostname}' successfully added to NetBox.")
    elif response.status_code == 400:
        print(f"⚠️ Failed to add device. Reason: {response.json()}")
    else:
        print(f"❌ Unexpected error. Status code: {response.status_code}, Response: {response.text}")

except NetmikoAuthenticationException:
    print("❌ Authentication failed. Check username/password.")
except NetmikoTimeoutException:
    print("❌ Timeout while connecting. Check IP or network.")
except Exception as e:
    print(f"❌ General error: {str(e)}")
