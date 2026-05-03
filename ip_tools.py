import speedtest

class SpeedTest:
    def __init__(self):
        self.st = speedtest.Speedtest()

    def speed_test(self):
        try:
            print("Finding best server...")
            self.st.get_best_server()
            download_speed = self.st.download() / 1_000_000  # Convert to Mbps
            upload_speed = self.st.upload() / 1_000_000  # Convert to Mbps
            ping = self.st.results.ping
            return download_speed, upload_speed, ping
        except Exception as e:
            print(f"An error occurred during the speed test: {e}")
            return None, None, None
        
# Example usage:
if __name__ == '__main__':
    tester = SpeedTest()
    download, upload, ping = tester.speed_test()
    if download and upload:
        print(f"Download speed: {download:.2f} Mbps")
        print(f"Upload speed: {upload:.2f} Mbps")
        print(f"Ping: {ping} ms")
