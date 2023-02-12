from flask import Flask, render_template, request
import serial
import json

app = Flask(__name__)

usb = serial.Serial("/dev/ttyACM0", baudrate=115200)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        # Convertir los datos a str antes de enviarlos
        slider1 = data.get('data1', None)
        slider2 = data.get('data2', None)
        slider3 = data.get('data3', None)
        slider4 = data.get('data4', None)
        #Crea una lista con los valores de los sliders que se han enviado
        sliders = [slider1,slider2,slider3,slider4]
        #unir los valores de los sliders en una sola cadena separados por comas
        slider_data = ','.join(map(str,sliders))
        print(f"\nSliders: {slider_data}")
        usb.write(f"{slider_data}\r\n".encode())
        return '', 204
    return render_template('index_sliders.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)

#@app.route('/')
#def index():
 #   return render_template('index_sliders.html')

#@app.route('/', methods=['POST'])
#def sliders():
 #   data = json.loads(request.data)
 #   print(data)

 #   usb.write(json.dumps(data).encode())
 #   return '',204
    