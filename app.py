from flask import Flask, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
import subprocess

try:
    while True:
        
        app = Flask(__name__)

        VLC_HOST = 'localhost'
        VLC_PORT = 8080
        VLC_PASSWORD = 'vlc'

        shutdown_flag = threading.Event()

        def get_vlc_status():
            url = f'http://{VLC_HOST}:{VLC_PORT}/requests/status.json'
            try:
                response = requests.get(url, auth=HTTPBasicAuth('', VLC_PASSWORD))
                if response.status_code == 200:
                    status_data = response.json()
                    if 'volume' in status_data:
                        web_volume = status_data['volume']
                        gui_volume = round((web_volume / 512) * 200)
                        status_data['gui_volume'] = gui_volume
                    return status_data
                else:
                    return {'error': f'HTTP {response.status_code}: Unable to connect to VLC'}
            except requests.exceptions.ConnectionError:
                return {'error': 'Connection error: Unable to connect to VLC'}
            except requests.exceptions.Timeout:
                return {'error': 'Timeout error: Unable to connect to VLC'}
            except requests.exceptions.RequestException as e:
                return {'error': f'Request error: {str(e)}'}

        @app.route('/vlc/status', methods=['GET'])
        def vlc_status():
            status = get_vlc_status()
            return jsonify(status)

        @app.route('/')
        def index():
            return render_template('index.html')

        def check_vlc_status_periodically():
            while not shutdown_flag.is_set():
                status = get_vlc_status()
                if status.get('state') == 'stopped':
                    

                    def close_vlc():
                        try:
                            subprocess.run(["taskkill", "/f", "/im", "vlc.exe"], check=True)
                            print("VLC has been closed.")
                        except subprocess.CalledProcessError as e:
                            print(f"Failed to close VLC: {e}")

                    if __name__ == "__main__":
                        close_vlc()

                    shutdown_system()
                    #alert_message()
                time.sleep(10)  # Check every 10 seconds

        def shutdown_system():
            if os.name == 'nt':
                os.system('shutdown /s /t 1')  # Windows shutdown command
            else:
                os.system('sudo shutdown -h now')  # Linux shutdown command
            shutdown_flag.set()  # Stop the periodic checking

        def alert_message():
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo("Info", "This is an information message.")


            



        if __name__ == '__main__':
            # Start the periodic check in a separate thread
            status_thread = threading.Thread(target=check_vlc_status_periodically)
            status_thread.start()

            app.run(debug=True, host='127.0.0.1', port=5000)

except KeyboardInterrupt:
    print("Program terminated by user")

