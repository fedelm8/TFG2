import subprocess
import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pwd
import shlex

# === CONFIGURACIÓN GENERAL ===
INTERVALO = 2  # segundos entre chequeos
CLAVE_ACCESO = "acceso_tarjetas"
CLAVE_DEFENSA = "clave_defensa"

ARCHIVO_SENSIBLE = os.path.expanduser("/home/osboxes/Documents/tarjetas_bancarias.txt")
SITIOS_RESTRINGIDOS = [
    "/etc/shadow", "/etc/passwd", "/etc/sudoers", "/root", "/boot", "/var/log",
    "/bin/bash", "/dev/mem", "/proc/kcore"
]
COMANDOS_PELIGROSOS = ["nmap", "tcpdump", "netstat", "bash", "nc", "rm", "chmod 777", "curl", "wget", "scp"]

# === RUTAS DE LOG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_ACCESOS = os.path.join(LOG_DIR, "accesos.log")
LOG_DEFENSA = os.path.join(LOG_DIR, "defense.log")

# === ESTADOS ===
eventos_acceso = set()
eventos_defensa = set()


# === FUNCIONES GENERALES ===
def registrar_log(path, usuario, ip):
    mensaje = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Usuario: {usuario} | IP: {ip}\n"
    try:
        with open(path, "a") as log_file:
            log_file.write(mensaje)
    except Exception as e:
        print(f"[X] Error al escribir en el log: {e}")

def enviar_alerta_gmail(asunto, mensaje):
    remitente = "pruebasfede1111@gmail.com"
    receptor = "pruebasfede1111@gmail.com"
    contrasena = "owbjrlluueabmpbf"  # contraseña de aplicación

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
        os.chmod(ARCHIVO_SENSIBLE, 0o000)
        print("[BLOQUEO] Permisos eliminados del archivo para impedir lectura.")
    except Exception as e:
        print(f"[X] Error al bloquear el archivo: {e}")


# === MONITOREO DE ACCESOS AL ARCHIVO SENSIBLE ===
def monitorear_accesos(timestamp):
    resultado = subprocess.run(
        ["ausearch", "-k", CLAVE_ACCESO, "-ts", timestamp, "--format", "raw"],
        stdout=subprocess.PIPE
    )
    logs = resultado.stdout.decode().split("\n\n")

    for log in logs:
        if log and log not in eventos_acceso:
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

            addr_line = next((line for line in log.splitlines() if "addr=" in line), None)
            if addr_line and "addr=" in addr_line:
                ip = addr_line.split("addr=")[-1].strip().split()[0]

            print("[ALERTA] ¡Intento de ACCESO DETECTADO al archivo sensible!")
            print(f"  ➤ Usuario: {usuario}")
            print(f"  ➤ IP: {ip}")
            registrar_log(LOG_ACCESOS, usuario, ip)
            bloquear_archivo()

            mensaje = f"""
Se ha detectado un intento de lectura en tarjetas_bancarias.txt

🔍 Detalles:
- Usuario: {usuario}
- IP: {ip}
- Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            enviar_alerta_gmail("ALERTA: Acceso al archivo sensible", mensaje)
            eventos_acceso.add(log)


# === MONITOREO DE ACCIONES SOSPECHOSAS ===
def monitorear_defensa(timestamp):
    resultado = subprocess.run(
        ["ausearch", "-k", CLAVE_DEFENSA, "-ts", timestamp, "--format", "raw"],
        stdout=subprocess.PIPE
    )
    logs = resultado.stdout.decode().split("\n\n")

    for log in logs:
        if log and log not in eventos_defensa:
            uid_line = next((line for line in log.splitlines() if "uid=" in line and "auid=" in line), None)
            uid = "desconocido"
            usuario = "desconocido"
            ip = "localhost"
            recurso = "indeterminado"

            if uid_line:
                try:
                    partes = uid_line.split()
                    for parte in partes:
                        if parte.startswith("uid="):
                            uid = int(parte.split("=")[1])
                            usuario = pwd.getpwuid(uid).pw_name
                except:
                    pass

            exe_line = next((line for line in log.splitlines() if "exe=" in line), None)
            if exe_line:
                try:
                    tokens = shlex.split(exe_line)
                    for token in tokens:
                        if token.startswith("exe="):
                            recurso = token.split("exe=")[-1]
                except Exception as e:
                    print(f"[X] Error al procesar exe_line: {exe_line} | {e}")

            addr_line = next((line for line in log.splitlines() if "addr=" in line), None)
            if addr_line and "addr=" in addr_line:
                ip = addr_line.split("addr=")[-1].strip().split()[0]

            path_lines = [line for line in log.splitlines() if "name=" in line]
            paths_accedidos = []
            for line in path_lines:
                try:
                    parts = line.split("name=")
                    if len(parts) > 1:
                        ruta = parts[1].split()[0].strip('"')
                        paths_accedidos.append(ruta)
                except Exception as e:
                    print(f"[X] Error al procesar línea PATH: {line} | {e}")

            accede_sitio_restringido = any(p in SITIOS_RESTRINGIDOS for p in paths_accedidos)

            if recurso == "/usr/bin/sudo":
                continue

            if accede_sitio_restringido or any(cmd in recurso for cmd in COMANDOS_PELIGROSOS):
                print("[DEFENSA] Actividad sospechosa detectada.")
                print(f"  ➤ Usuario: {usuario}")
                print(f"  ➤ IP: {ip}")
                print(f"  ➤ Recurso: {recurso}")
                print(f"  ➤ Rutas accedidas: {paths_accedidos}")
                registrar_log(LOG_DEFENSA, usuario, ip)

                rutas_txt = "\n".join(f"  - {ruta}" for ruta in paths_accedidos) if paths_accedidos else "  - No determinado"
                mensaje = f"""
Se ha detectado una posible intrusión o acceso no permitido al sistema operativo.

🔍 Detalles:
- Usuario: {usuario}
- IP: {ip}
- Recurso ejecutado: {recurso}
- Recursos accedidos:
{rutas_txt}
- Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                enviar_alerta_gmail("🚨 ALERTA DE SEGURIDAD: Acceso sospechoso al sistema", mensaje)
                eventos_defensa.add(log)


# === PROCESO PRINCIPAL ===
if __name__ == "__main__":
    print("[*] Sistema de monitoreo unificado iniciado.")
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[*] Ignorando eventos anteriores a {timestamp}\n")

    try:
        while True:
            monitorear_accesos(timestamp)
            monitorear_defensa(timestamp)
            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n[+] Monitor finalizado por el usuario. Cerrando...")
