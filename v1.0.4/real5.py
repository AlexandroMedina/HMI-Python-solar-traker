import pvlib
import numpy as np
import pandas as pd
import tkinter as  tk
from tkinter import ttk 
import serial, serial.tools.list_ports, sys

#funcion para validar que solo entren caracteres para una fecha
def fecha_valida(action, char, text):
        # Solo chequear cuando se añade un carácter.
        if action != "1":
                return True
        return char in "0123456789-" and len(text) < 10
#Funcion para solo dejar enteros y un caracter especial con un limite de caracteres
def enteros(action, char, text):
        # Solo chequear cuando se añade un carácter.
        if action != "1":
                return True
        return char in "0123456789.-" and len(text) < 8
#funcio para dejar entarr slo dos caracteres para la hora y minutos
def hora_validada(action, char, text):
      if action !="1":
            return True
      return char in "0123456789:" and len (text) < 5

class Application(tk.Frame):
    
    def conectar_puerto(self):
        puerto_seleccionado = self.combo_puertos.get()
        baudios_seleccionados = int(self.combo_baudios.get())   
        try:
                # Crear una instancia del objeto Serial
                global puerto_serial
                puerto_serial = serial.Serial(port=puerto_seleccionado, baudrate=baudios_seleccionados, timeout=2, write_timeout=2)
                #time.sleep(3)
                print("Conexión exitosa al puerto:", puerto_seleccionado)
                self.var1.config(state='normal')
                self.var2.config(state='normal')
                self.var3.config(state='normal')
                self.var4.config(state='normal')
                self.var5.config(state='normal')

        except serial.SerialException:
                print("Error al conectar al puerto:", puerto_seleccionado)

    def escribir_puerto(self):
        dato1 = str(self.azimuth_solar)
        dato2 = str(self.ang_elevacion)
        resultado_serial = str(dato1 + " " + dato2)
        puerto_serial.write(resultado_serial.encode('utf-8'))
        print(resultado_serial)

#Funcion para adquiriri los datos que se ingresen en los "Entry"
    def borrar_contenido(self):
        self.var1.delete(0, tk.END)
        self.var2.delete(0, tk.END)
        self.var3.delete(0, tk.END)
        self.var4.delete(0, tk.END)
        self.var5.delete(0, tk.END)
        self.label9["text"] = ""
        
#funcion para inciar una clase de Python
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Posicionar elementos")
        main_window.resizable(0,0)
        main_window.configure(width=380, height=465)        
        self.place(relwidth=1, relheight=1)

        self.label0 = ttk.Label(self, text="¡Posicionamiento solar!", font="Arial")
        self.label0.place(x=120, y=10)
#puerto a seleccionar
        self.combo_puertos = ttk.Combobox(self, state="readonly", width=10)
        self.combo_puertos ['values'] = [port.device for port in serial.tools.list_ports.comports()]
        self.combo_puertos.place(x=50, y=40)         
#baudios seleccionados
        self.combo_baudios = ttk.Combobox(self, state="readonly", width=10)
        self.combo_baudios['values'] = ['9600', '19200', '31250', '38400', '115200']
        self.combo_baudios.current(4)
        self.combo_baudios.place(x=150, y=40)
#Boton para conectar
        self.conectar = ttk.Button(self, text="Conectar", cursor="star", command=self.conectar_puerto)
        self.conectar.place(x=250, y=38)
#Latitud
        self.label1 = ttk.Label(self, text="Latitud:", font="Arial")
        self.label1.place(x=50, y=70)        
        
        validatecommand = main_window.register(enteros)
        self.var1 = ttk.Entry(self, validate="key", validatecommand=(validatecommand, "%d", "%S", "%P"), state='disabled')
        self.var1.place(x=190, y=70)
#Longitud local:
        self.label2 = ttk.Label(self, text="Longitud:", font="Arial")
        self.label2.place(x=50, y=110)
        
        self.var2 = ttk.Entry(self, validate="key", validatecommand=(validatecommand, "%d", "%S", "%P"), state='disabled')
        self.var2.place(x=190, y=110)
#Longitud estandar:
        self.label3 = ttk.Label(self, text="         Introduce la zona horaria \n(por ejemplo, 'America/Mexico_City'):", font="Arial")
        self.label3.place(x=50, y=140)
        
        self.var3 = ttk.Entry(self, state='disabled')
        self.var3.place(x=140, y=185)
#Ingrese fecha "aaaa/mm/dd
        self.label4 = ttk.Label(self, text="Ingrese fecha AAAA-MM-DD", font="Arial")
        self.label4.place(x=100, y=215)
        
        validatecommand = main_window.register(fecha_valida)
        self.var4 = ttk.Entry(self, validate="key", validatecommand=(validatecommand, "%d", "%S", "%s"), state='disabled')
        self.var4.place(x=140, y=240)             
#Para la hora estandar indicar por separado la hora y los minutos
        self.label5 = ttk.Label(self, text="Introduce la hora de formato en 24hrs 'HH:MM' ):", font="Arial")
        self.label5.place(x=30, y=270)
    #Hora     
        validatecommand = main_window.register(hora_validada)
        self.var5 = ttk.Entry(self, validate="key", validatecommand=(validatecommand, "%d", "%S", "%s"), state='disabled')
        self.var5.place(x=140, y=300)
#Boton calcular
        self.calcular = ttk.Button(self, text="Calcular", cursor="star", command=self.mostrar_valor)
        self.calcular.place(x=50, y=340)
#Boton finalizar
        self.cerrar = ttk.Button(self, text="Cerrar", cursor="plus", command=self.finalizar)
        self.cerrar.place(x=150, y=340)
#Boton Limpiar casillas
        self.limpiar = ttk.Button(self, text="LImpiar", cursor="star", command=self.borrar_contenido)
        self.limpiar.place(x=250, y=340)
#Label resultado
        self.label9 = ttk.Label(self, font=("Arial", 14), state="disabled", anchor="center")
        self.label9.place(x=90, y= 380)
#Boton para enviar los datos al puert serial
        self.enviar = ttk.Button(self, text="Enviar", cursor="plus", command=self.escribir_puerto)
        self.enviar.place(x=150, y=425)

#Funcion para cerrar correctamente el puerto y la ventana creada
    def finalizar(self): 
        print("Puerto serial cerrado")
        puerto_serial.close()
        sys.exit(0)
#Funcion para calcular el azimuth, agulo de elevacion y mosrtralo en el label9
    def mostrar_valor(self):
        latitude = float(self.var1.get())
        longitude = float(self.var2.get())
        tz = self.var3.get()
        date_str = self.var4.get()
        hour_str = self.var5.get()
        date_time = pd.Timestamp(f"{date_str} {hour_str}", tz=tz)
# Calcula la posicion solar
        solar_position = pvlib.solarposition.get_solarposition(date_time, latitude, longitude)
#Calcular azimuth
        azimuth = solar_position['azimuth']
        azimuth = np.radians(azimuth)  # Convierte a radianes
#Calcular angulo de elevacion        
        elevation = np.radians(solar_position['apparent_elevation'])
#Conversion a grados
        elevation_degrees = np.degrees(elevation)
        azimuth_degrees = np.degrees(azimuth)
#Redondeamos valores 
        self.azimuth_solar =  round(azimuth_degrees[0], 4) # Accede al valor numérico en el índice 0
        self.ang_elevacion = round(elevation_degrees[0],4)  # Accede al valor numérico en el índice 0
        resultado = "Azimutal grados: {}\nElevación en grados: {}".format(self.azimuth_solar, self.ang_elevacion)
        self.label9["text"] =  resultado

main_window = tk.Tk()
app = Application(main_window)
app.config(bg="snow3")
app.mainloop()