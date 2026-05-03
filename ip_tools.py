import requests
import socket
import subprocess
import platform

def get_ip_info(ip):
    """Get IP geolocation info"""
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            data = response.json()
            return f"""
🌍 **IP Information for {ip}**
Country: {data.get('country_name', 'N/A')}
City: {data.get('city', 'N/A')}
Region: {data.get('region', 'N/A')}
ISP: {data.get('org', 'N/A')}
Timezone: {data.get('timezone', 'N/A')}
Latitude: {data.get('latitude', 'N/A')}
Longitude: {data.get('longitude', 'N/A')}
            """
    except Exception as e:
        return f"❌ Error: {str(e)}"

def speed_test():
    """Run speed test"""
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        return f"""
📊 **Speed Test Results**
Download: {download:.2f} Mbps
Upload: {upload:.2f} Mbps
Ping: {ping:.2f} ms
        """
    except Exception as e:
        return f"❌ Error: {str(e)}"

def ping_host(host):
    """Ping a host"""
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output(['ping', '-n', '4', host])
        else:
            output = subprocess.check_output(['ping', '-c', '4', host])
        return f"✅ **Ping to {host}**\n```\n{output.decode()}\n```"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_ip_type(ip):
    """Analyze IP type"""
    try:
        parsed_ip = socket.inet_aton(ip)
        first_octet = int(ip.split('.')[0])
        
        ip_type = "Public"
        if first_octet in [10] or ip.startswith('172.16.') or ip.startswith('192.168.'):
            ip_type = "Private"
        
        return f"""
🔍 **IP Type Analysis for {ip}**
Type: {ip_type}
Version: IPv4
        """
    except Exception as e:
        return f"❌ Error: {str(e)}"
