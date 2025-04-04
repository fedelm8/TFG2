import subprocess
import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pwd  # Para traducir UID a nombre de usuario

ARCHIVO = os.path.expanduser("/home/osboxes/Documents/tarjetas_bancarias.txt")
CLAVE = "acceso_tarjetas"
INTERVALO = 2  # Segundos entre chequeos

# Ruta del log en carpeta 'logs' junto al script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_PATH = os.path.join(LOG_DIR, "accesos.log")

# Crear carpeta logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

eventos_detectados = set()

def registrar_log(usuario, ip):
    mensaje = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Usuario: {usuario} | IP: {ip}\n"
    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(mensaje)
    except Exception as e:
        print(f"[X] Error al escribir en el log: {e}")

def enviar_alerta_gmail(usuario, ip):
    remitente = "pruebasfede1111@gmail.com"
    receptor = "pruebasfede1111@gmail.com"
    asunto = "ALERTA: Acceso al archivo sensible"
    mensaje = f"""
Se ha detectado un intento de lectura en tarjetas_bancarias.txt

🔍 Detalles:
- Usuario: {usuario}
- IP: {ip}
- Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    ##contrasena = "grkyynyhfuxecing"  #contraseña de aplicación
    contrasena = "gsxacdvzlnelgitx"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = receptor
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje, "plain"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contrasena)
        servidor.sendmail(remitente, receptor, msg.as_string())
        servidor.quit()
        print("[EMAIL] Alerta enviada por correo.")
    except Exception as e:
        print(f"[X] Error al enviar correo: {e}")

def bloquear_archivo():
    try:
        os.chmod(ARCHIVO, 0o000)
        print("[BLOQUEO] Permisos eliminados del archivo para impedir lectura.")
    except Exception as e:
        print(f"[X] Error al bloquear el archivo: {e}")

def monitorear_accesos():
    print(f"[*] Monitoreando accesos de lectura al archivo:\n{ARCHIVO}\n")

    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[*] Ignorando eventos anteriores a {timestamp}\n")

    try:
        while True:
            resultado = subprocess.run(
                ["ausearch", "-k", CLAVE, "-ts", timestamp, "--format", "raw"],
                stdout=subprocess.PIPE
            )
            logs = resultado.stdout.decode().split("\n\n")

            for log in logs:
                if log and log not in eventos_detectados:
                    # Extraer UID
                    uid_line = next((line for line in log.splitlines() if "uid=" in line and "auid=" in line), None)
                    uid = "desconocido"
                    usuario = "desconocido"
                    ip = "localhost"

                    if uid_line:
                        try:
                            partes = uid_line.split()
                            for parte in partes:
                                if parte.startswith("uid="):
                                    uid = int(parte.split("=")[1])
                                    usuario = pwd.getpwuid(uid).pw_name
                        except:
                            pass

                    # Extraer IP 
                    addr_line = next((line for line in log.splitlines() if "addr=" in line), None)
                    if addr_line and "addr=" in addr_line:
                        ip = addr_line.split("addr=")[-1].strip().split()[0]

                    print("[ALERTA] ¡Intento de ACCESO DETECTADO al archivo sensible!")
                    print(f"  ➤ Usuario: {usuario}")
                    print(f"  ➤ IP: {ip}")
                    registrar_log(usuario, ip)
                    bloquear_archivo()
                    enviar_alerta_gmail(usuario, ip)
                    eventos_detectados.add(log)

            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n[+] Monitor finalizado por el usuario. Cerrando...")

if __name__ == "__main__":
    monitorear_accesos()

