# Herramienta de Monitoreo de Accesos a Archivos Sensibles

## Descripción

Esta herramienta monitorea en tiempo real los accesos a archivos sensibles del sistema, como `/etc/shadow` y `/etc/passwd`, que son comúnmente utilizados para la gestión de contraseñas y usuarios en sistemas Linux. 

Cuando la herramienta detecta un intento de acceso no autorizado a estos archivos, realiza las siguientes acciones:
- Envía una alerta por correo electrónico.
- Bloquea el proceso relacionado con el acceso, si es necesario.

La herramienta se ejecuta como un servicio en segundo plano mediante **`systemd`**, lo que permite que se ejecute de manera continua incluso después de reiniciar el sistema.

---

## **Requisitos**

### **Dependencias del sistema**
1. **`auditd`**: Necesario para auditar los accesos a archivos sensibles.
   - Instalación:
     ```bash
     sudo apt-get install auditd
     ```

2. **Python 3.x**: Necesario para ejecutar los scripts.
   - Asegúrate de tener Python 3 instalado.
   - Puedes verificar la versión de Python con:
     ```bash
     python3 --version
     ```

3. **Bibliotecas de Python** (si las necesitas):
   Si la herramienta requiere bibliotecas adicionales, instala las dependencias con:
   ```bash
   pip install -r requirements.txt

# Monitoring_tool

*Secure your data, empower your peace of mind.*

![Last Commit](https://img.shields.io/badge/last%20commit-today-brightgreen)
![Python](https://img.shields.io/badge/python-100%25-blue)
![Languages](https://img.shields.io/badge/languages-1-blue)

_Built with the tools and technologies:_

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)

---

## Overview

**monitoring_tool** is a robust monitoring tool designed to safeguard sensitive files by detecting unauthorized access in real-time.

### Why monitoring_tool?

This project enhances system security by providing continuous oversight of critical files. The core features include:

- 🔐 **Real-time Monitoring**: Instantly detects unauthorized access attempts to sensitive files.
- 🚨 **Alerts**: Automatically alerts administrators and blocks suspicious processes to prevent breaches.
- 🔄 **Continuous Operation**: Runs as a background service, ensuring ongoing surveillance even after system reboots.
- 👤 **User Logging**: Captures user details and IP addresses for accountability and traceability.
- ⚙️ **Systemd Integration**: Simplifies deployment with automatic service management for Linux systems.

---

## Getting Started

### Prerequisites

- `Python 3.x`
- `pip`
- `systemd` : to execute automatically the script. 
- `Gmail (SMTP)` : for sending the alert.
- `auditd` : for detecting file accesses.

### Installation

```bash
git clone https://github.com/tuusuario/TFG2.git
cd TFG2
pip install -r requirements.txt

#Install auditd
sudo apt update
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd

##Instal git and Python3
sudo apt install -y git python3 python3-pip

cd Documents

##Clone Github repository in Documents
git clone https://github.com/fedelm8/TFG2

##Create the delicate file
sudo nano tarjetas_bancarias.txt
sudo chmod 644 tarjetas_bancarias.txt

##Add temporal audit tool for testing
sudo auditctl -w /home/osboxes/Documents/tarjetas_bancarias.txt -p r -k acceso_tarjetas

##Make it permanent
sudo nano /etc/audit/rules.d/monitor.rules
##File content
-w /home/osboxes/Documents/tarjetas_bancarias.txt -p r -k acceso_tarjetas
##Aply rule
sudo augenrules --load
sudo systemctl restart auditd
##Check the rule
sudo auditctl -l

##Prepare Gmail
##Open Internet:
##https://myaccount.google.com/security
#Create app password
##https://myaccount.google.com/apppasswords
##Name: monitor_tarjetas
##Copy the key (ex: grkyy nyhf uxec iing)

##Change password that we copied before
sudo nano monitor_tarjetas.py

##Save script in a protected file (only for sudo)
sudo mkdir -p /opt/monitor_archivo
sudo cp monitor_tarjetas.py /opt/monitor_archivo/
sudo chmod 700 /opt/monitor_archivo/monitor_tarjetas.py
sudo chown root:root /opt/monitor_archivo/monitor_tarjetas.py


##Turn it into a systemd service

sudo nano /etc/systemd/system/monitor_tarjetas.service

##Content:
[Unit]
Description=Monitor de accesos a archivo sensible
After=network.target auditd.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/monitor_archivo/monitor_tarjetas.py
Restart=on-failure
User=root
Group=root

[Install]
WantedBy=multi-user.target


##Start the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable monitor_tarjetas.service
sudo systemctl start monitor_tarjetas.service

##Verify

sudo systemctl status monitor_tarjetas.service
