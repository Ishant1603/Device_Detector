
from flask import Flask,render_template, jsonify,request
from services.email import *
from services.wifi import *

app = Flask(__name__)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-ip/" ,methods=["get","post"])
def scan_network():
    if request.method=="POST":
        try:
            ip=request.get_json().get("ip","")
            print(ip)
    
            if not ip:
                return jsonify({
                    "error":"invlid Ip"
                }), 400
            
           
            # with ThreadPoolExecutor() as executor:
            #     future = executor.submit(scan, ip)
            #     try:
            #         current_devices = future.result(timeout=5)  # Timeout in seconds
            #     except TimeoutError:
            #         return jsonify({"error": "Scanning timed out"}), 408
           
           
           
            current_devices = scan(ip)
            previous_devices = load_devices()

            new_devices = [device for device in current_devices if device not in previous_devices]
            
            if new_devices:
                save_devices(current_devices)

                send_email(new_devices)
                send_notification(new_devices)
            print(current_devices)
            if not current_devices:
                return jsonify({
                    "error":"no ips found"
                }),400
            
            return jsonify({
                "data":current_devices
            }),200
        except Exception as e:
            print(e)
            return jsonify({
                "error":"an error occred"
            }),400
    else:
        return jsonify({
            "error":"method not allowed"
        }),400


if __name__ == "__main__":
    app.run(debug=True,port=5001)
