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

# TFG2

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

**TFG2** is a robust monitoring tool designed to safeguard sensitive files by detecting unauthorized access in real-time.

### Why TFG2?

This project enhances system security by providing continuous oversight of critical files. The core features include:

- 🔐 **Real-time Monitoring**: Instantly detects unauthorized access attempts to sensitive files.
- 🚨 **Alerts & Blocks**: Automatically alerts administrators and blocks suspicious processes to prevent breaches.
- 🔄 **Continuous Operation**: Runs as a background service, ensuring ongoing surveillance even after system reboots.
- 👤 **User Logging**: Captures user details and IP addresses for accountability and traceability.
- ⚙️ **Systemd Integration**: Simplifies deployment with automatic service management for Linux systems.

---

## Getting Started

### Prerequisites

- Python 3.8+
- `pip`
- `systemd` (for Linux-based deployments)

### Installation

```bash
git clone https://github.com/tuusuario/TFG2.git
cd TFG2
pip install -r requirements.txt
