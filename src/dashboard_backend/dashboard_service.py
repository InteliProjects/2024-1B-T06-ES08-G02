from flask import Flask, jsonify, render_template, request
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
app.config['LOG_FILE'] = '../ecm_backend/upload_log.txt'


def get_upload_logs(start_date=None, end_date=None):
    logs = []
    if os.path.exists(app.config['LOG_FILE']):
        with open(app.config['LOG_FILE'], 'r') as log_file:
            for line in log_file:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    name, date_str, size, type, erro_forjado, upload_speed = parts
                    try:
                        date = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
                        if start_date and end_date:
                            if not (start_date <= date <= end_date):
                                continue
                        logs.append({
                            "name": name,
                            "date": date_str,
                            "size": size,
                            "type": type,
                            "erro_forjado": erro_forjado == 'True',
                            "upload_speed": float(upload_speed)
                        })
                    except ValueError:
                        print(f"Data no formato incorreto: {date_str}")
    return logs

@app.route('/monitor')
def monitor():
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    logs = get_upload_logs(start_date, end_date)
    uploads_per_day = defaultdict(int)
    errors_per_day = defaultdict(int)
    upload_speeds = defaultdict(list)

    for log in logs:
        date = log['date'].split()[0]  
        uploads_per_day[date] += 1
        if log['erro_forjado']:
            errors_per_day[date] += 1
        upload_speeds[date].append(log['upload_speed'])

    
    average_speeds_per_day = {date: sum(speeds) / len(speeds) for date, speeds in upload_speeds.items()}

    data = {
        "uploads_per_day": uploads_per_day,
        "errors_per_day": errors_per_day,
        "average_speeds_per_day": average_speeds_per_day,
        "logs": logs  
    }
    return jsonify(data)

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
