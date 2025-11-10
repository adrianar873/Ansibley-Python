from flask import Flask, jsonify, request
from pymongo.errors import ServerSelectionTimeoutError
from apscheduler.schedulers.background import BackgroundScheduler
from system_info import SystemMonitor

app = Flask(__name__)
monitor = SystemMonitor("mongodb://localhost:27017/", "system_monitor", "servers_metrics")

@app.route("/")
def home():
    return jsonify({
        "message": "System Monitor API",
        "host": monitor.hostname,
        "endpoints": ["/system", "/cpu", "/memory", "/disk", "/network", "/processes", "/send", "/all"]
    })

@app.route("/system")
def system():
    return jsonify(monitor.get_system_info())

@app.route("/cpu")
def cpu():
    return jsonify(monitor.get_cpu_info())

@app.route("/memory")
def memory():
    return jsonify(monitor.get_memory_info())

@app.route("/disk")
def disk():
    return jsonify(monitor.get_disk_info())

@app.route("/network")
def network():
    return jsonify(monitor.get_network_info())

@app.route("/processes")
def processes():
    return jsonify(monitor.get_processes(int(request.args.get("limit", 10))))

@app.route("/all")
def all_metrics():
    return jsonify(monitor.get_all_metrics(int(request.args.get("limit", 10))))

@app.route("/send")
def send():
    try:
        monitor.send_all_metrics()
        return jsonify({"status": "success", "msg": "Datos enviados", "host": monitor.hostname})
    except ServerSelectionTimeoutError:
        return jsonify({"status": "error", "msg": "No se pudo conectar a MongoDB"}), 500
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


if __name__ == "__main__":
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=monitor.send_all_metrics, trigger="interval", minutes = 30)
    scheduler.start()

    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        monitor.close_connection()
    