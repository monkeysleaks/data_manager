import winsound
ruta_sonido = "C:/Users/diego/Desktop/windows-notify.wav"
winsound.PlaySound(ruta_sonido, winsound.SND_FILENAME)

def main():
    while True:
        print('''1.- subir voe
2.- subir filemoon
3.- agregar datos
4.- actualizar datos
5.- crear previews
6.- subir previews
7.- rebuild cloudflare

''')