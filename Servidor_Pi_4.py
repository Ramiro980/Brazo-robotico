from flask import Flask, render_template, request
import serial
import json
import time

app = Flask(__name__, static_folder='static')

usb = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return 'Datos inválidos', 400

        # Obtiene los valores de los sliders
        slider1 = data.get('data1', 90)
        slider2 = data.get('data2', 90)
        slider3 = data.get('data3', 90)
        slider4 = data.get('data4', 0)

        # Forma el mensaje en formato: "90,90,90,1"
        slider_data = f"{slider1},{slider2},{slider3},{slider4}\r\n"
        print(f"Sliders: {slider_data.strip()}")

        if usb:
            try:
                usb.write(slider_data.encode())
            except Exception as e:
                print(f"Error al enviar datos por serial: {e}")
                return 'Error serial', 500

        return '', 204

    return render_template('index_sliders.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#@app.route('/')
#def index():
 #   return render_template('index_sliders.html')

#@app.route('/', methods=['POST'])
#def sliders():
 #   data = json.loads(request.data)
 #   print(data)

 #   usb.write(json.dumps(data).encode())
 #   return '',204
    
