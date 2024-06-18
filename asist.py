import io
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from pynput.keyboard import Key,Controller
import time
import re
import tkinter as tk
from tkinter import filedialog as fd
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
import sys
import keyboard as k


keyboard = Controller()
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'


def volumenup(n):
    for i in range(int(n-(n/3))):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        time.sleep(0.1)


def volumendown(n):
    for i in range(int(n-(n/3))):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        time.sleep(0.1)


# escuchar microfono y devolver audio como texto
def transform_audio_text():
    # almacenar recognizer en una variable
    r = sr.Recognizer()
    r.energy_threshold = 4000
    # r.dynamic_energy_threshold = True
    # configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.6
        # ajustar para ruido del ambiente
        r.adjust_for_ambient_noise(origen, duration=0.8)
        # informar inicio grabacion
        print('you can speak now')
        # guradar lo que escuche
        # audio = r.listen(origen)
        audio = r.record(origen, duration=5)
        try:
            # buscar en google
            pedido = r.recognize_google(audio, language='es-co')
            pedido = pedido.lower()
            # prueba de que se reconoce
            print('you said: ' + pedido)
            # devolver pedido
            return pedido
        # si no se puede reconocer el audio
        except sr.UnknownValueError:
            # prueba de que no se comprende el audio
            print("I can't understand")
            return 'retry'
        # si no se puede resolver el pedido
        except sr.RequestError:
            # prueba de que no se comprende el audio
            print("No service")
            return 'retry'
        except:
            print("Nothing")
            return 'retry'


# funcion para hablar desde el asistente
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    # cambiar voz
    # engine.setProperty('voice', id1)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# voces disponibles
def ver_opciones_de_voz():
    engine = pyttsx3.init()
    for voz in engine.getProperty('voices'):
        print(voz)


# informar el dia de la semana
def pedir_dia():
    #crear variable con datso de hoy
    dia = datetime.date.today()
    #print(dia)
    # variable dia de la semana
    dia_s = dia.weekday()
    #print(dia_s)
    #diccionario nombres de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    #decir dia
    hablar(f'Hoy es {calendario[dia_s]}')


def pedir_fecha():
    dia = datetime.date.today()
    hablar(f'La fecha de hoy es {dia}')


# informar hora
def pedir_hora():
    # variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momentos son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    #print(hora)
    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():
    # decir saludo
    hora = datetime.datetime.now()
    if 18 < int(hora.hour) < 24:
        h = 'Buenas noches'
    elif 0 < int(hora.hour) < 12:
        h = 'Buenos dias'
    else:
        h = 'Buenas tardes'
    hablar(f'Hola Hans, {h}')


def welcome_hans():
    saludo_inicial()
    pedir_dia()
    pedir_hora()


def buscar_navegador(s):
    driver = webdriver.Edge()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{s}")
    search_box.send_keys(Keys.RETURN)


def browse_pdf():
    filename = fd.askopenfilename(filetypes=(("Archivos PDF", "*.pdf*"),
                                             ("Todos los archivos", "*.*")))
    return filename


# funcion central
def pedir_cosas():
    saludo_inicial()
    #variable de corte
    comenzar = True
    #loop
    while comenzar:

        pedido = transform_audio_text().lower()
        if 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            try:
                resultado = wikipedia.summary(pedido, sentences=10)
            except:
                hablar('No hay coincidencias de resultado en wikipedia')
                continue
            else:
                hablar('este es el resultado de wikipedia')
                hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Buscando, un momento porfavor')
            pedido = pedido.replace('busca en internet', '')
            try:
                pywhatkit.search(pedido)
            except:
                hablar('No hay coincidencias de resultado en internet')
                continue
            else:
                hablar('Este es el resultado de la busqueda')
            """
            pedido = pedido.replace('busca en internet', '')
            hablar(f'con gusto, buscando {pedido} en google')
            webbrowser.open(f'https://www.google.com/search?q={pedido}&oq={pedido}&gs_lcrp=EgZjaHJvbWUyEQgAEEUYORhDGLEDGIAEGIoFMgwIARAAGEMYgAQYigUyDAgCEAAYQxiABBiKBTIMCAMQABhDGIAEGIoFMg8IBBAAGEMYsQMYgAQYigUyCggFEAAYsQMYgAQyBwgGEAAYgAQyDQgHEAAYsQMYyQMYgATSAQc4MzZqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8')
            """
            #buscar_navegador(pedido)
            continue
        elif 'abre' in pedido and 'navegador' in pedido:
            hablar('con gusto, abro el navegador')
            webbrowser.open('https://www.google.com')
            continue
        elif 'hora' in pedido:
            pedir_hora()
            continue
        elif 'fecha' in pedido:
            pedir_fecha()
            continue
        elif 'día' in pedido:
            pedir_dia()
            continue
        elif 'cierra' in pedido and 'navegador' in pedido:
            hablar('cerrando el navegador')
            os.system('taskkill/im msedge.exe /F')
            continue
        elif 'abre la aplicación' in pedido:
            pedido = pedido.replace('abre la aplicación', '')
            hablar(f'con gusto, abriendo {pedido}')
            os.system(f'start {pedido}')
            continue
        elif 'sube el volumen' in pedido:
            hablar('subiendo el volumen')
            numeros = re.findall("\d+", pedido)
            volumenup(int(numeros[0]))
            continue
        elif 'baja el volumen' in pedido:
            hablar('bajando el volumen')
            numeros = re.findall("\d+", pedido)
            volumendown(int(numeros[0]))
            continue
        elif 'reproducir' in pedido:
            hablar('¡Vale!, ahora mismo reproduzco la canción')
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            break
        elif 'abrir la página' in pedido:
            pedido = pedido.replace('abrir la página', '')
            hablar(f'¡Vale!, abriendo la pagina {pedido}')
            pedido = pedido+'.com'
            webbrowser.open(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except Exception as err:
                hablar('No encontre coincidencias de la busqueda')
                print(err)
                continue
        elif 'mac' in pedido:
            os.system('cmd /c "getmac"')
            continue
        elif 'ip' in pedido:
            os.system('cmd /c "ipconfig"')
            continue
        elif 'leer pdf' in pedido:
            ruta = browse_pdf()
            print(ruta)
            try:
                archivo = open(ruta, 'rb')
                webbrowser.open(ruta)
                parser = PDFParser(archivo)
                documento = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                reconocedor = sr.Recognizer()
                motor = pyttsx3.init()
                buffer = io.BytesIO()
                motor.setProperty("output_device_index", -1)
                # motor.audio_engine.setProperty("output", buffer)
                while True:
                    for pagina in PDFPage.create_pages(documento):
                        if not k.is_pressed('esc'):
                            interpreter.process_page(pagina)
                            layout = device.get_result()
                            for objeto in layout:
                                if isinstance(objeto, LTTextBox):
                                    texto = objeto.get_text()
                                    print(texto)
                                    motor.say(texto)
                            motor.runAndWait()
                        else:
                            break
                    buffer.close()
                    audio = buffer.getvalue()
                    archivo_audio = sr.AudioFile(audio)
                    with archivo_audio as fuente:
                        audio = reconocedor.record(fuente)
                    try:
                        texto = reconocedor.recognize_google(audio, language="es-CO")
                        print("Texto reconocido:")
                        print(texto)
                    except sr.UnknownValueError:
                        print("No se pudo reconocer el audio")
                    except sr.RequestError as e:
                        print(f"Error al llamar al servicio de Google; {e}")
            except Exception as err:
                print(err)
        elif 'opciones de voz' in pedido:
            ver_opciones_de_voz()
            continue
        elif 'cambia la voz' in pedido:
            voz = pedido.split('opción')[-1].strip()
            engine = pyttsx3.init()
            if voz == 2 or voz == '2' or voz == 'dos':
                engine.setProperty('voice', id2)
                hablar('Esta es mi nueva voz')
                continue
            else:
                engine.setProperty('voice', id1)
                hablar('Esta es mi nueva voz')
                continue
        elif 'sesión' in pedido:
            hablar('Hasta pronto, fue un gusto atenderte')
            break


def main():
    while True:
        try:
            pedir_cosas()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass
        else:
            sys.exit(0)
        finally:
            sys.exit(0)


if __name__ == '__main__':
    main()











'''
bloquear pc desde cmd
rundll32.exe user32.dll, LockWorkStation
'''