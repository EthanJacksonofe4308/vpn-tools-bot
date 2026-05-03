import json
import os

VPN_DB = 'vpn_data.json'

def load_vpn_list():
    if os.path.exists(VPN_DB):
        with open(VPN_DB, 'r') as f:
            return json.load(f)
    return []

def save_vpn_list(vpn_list):
    with open(VPN_DB, 'w') as f:
        json.dump(vpn_list, f, indent=2)

def add_vpn(name, link):
    vpn_list = load_vpn_list()
    vpn_list.append({'name': name, 'link': link})
    save_vpn_list(vpn_list)
    return f"✅ Added VPN: {name}"

def get_vpn_list():
    vpn_list = load_vpn_list()
    if not vpn_list:
        return "No VPN links saved yet"
    
    text = "🔗 **VPN List**\n"
    for i, vpn in enumerate(vpn_list, 1):
        text += f"{i}. {vpn['name']}\n`{vpn['link']}`\n\n"
    return text
