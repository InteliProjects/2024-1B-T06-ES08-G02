import threading
import subprocess

def start_upload_service():
    try:
        subprocess.run(["python", "upload_service.py"], cwd="src/ecm_backend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o serviço de upload: {e}")

def start_dashboard_service():
    try:
        subprocess.run(["python", "dashboard_service.py"], cwd="src/dashboard_backend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o serviço de dashboard: {e}")

def start_measurement_service():
    try:
        subprocess.run(["python", "measurement_service.py"], cwd="src/measurement_backend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o serviço de medição: {e}")

if __name__ == "__main__":
    upload_thread = threading.Thread(target=start_upload_service)
    dashboard_thread = threading.Thread(target=start_dashboard_service)
    measurement_thread = threading.Thread(target=start_measurement_service)

    upload_thread.start()
    dashboard_thread.start()
    measurement_thread.start()

    upload_thread.join()
    dashboard_thread.join()
    measurement_thread.join()
