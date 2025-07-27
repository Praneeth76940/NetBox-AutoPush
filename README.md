## NetBox Auto Discovery & Push

This project discovers Cisco devices and automatically pushes data to NetBox using Python, Netmiko, and the NetBox REST API.

### Features
- SSH into Cisco routers/switches using Netmiko
- Auto-discover hostname, management IP, and interfaces
- Push device & interface data to NetBox DCIM

### Structure
- `scripts/discover_and_push.py`: Push device info
- `scripts/push_interfaces.py`: Push interface info

### Requirements
- Python 3.x
- `pip install -r requirements.txt`

### Usage
```bash
python3 scripts/discover_and_push.py
python3 scripts/push_interfaces.py
