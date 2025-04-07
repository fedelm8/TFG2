
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
- [Prerequisites](#prerequisites)
- [Installation and Usage](#installation-and-usage)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

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

## Prerequisites

- Python 3.x  
- `pip`  
- `systemd`: to execute the script automatically  
- Gmail (SMTP): for sending alerts  
- `auditd`: for detecting file accesses  

---

## Installation and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/tuusuario/TFG2.git
cd TFG2
pip install -r requirements.txt
```

### 2. Install `auditd`

```bash
sudo apt update
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd
```

### 3. Install Git and Python3

```bash
sudo apt install -y git python3 python3-pip
```

### 4. Clone the Project

```bash
cd ~/Documents
git clone https://github.com/fedelm8/TFG2
```

### 5. Create a Sensitive File to Monitor

```bash
sudo nano tarjetas_bancarias.txt
sudo chmod 644 tarjetas_bancarias.txt
```

### 6. Add Temporary Audit Rule for Testing

```bash
sudo auditctl -w /home/osboxes/Documents/tarjetas_bancarias.txt -p r -k acceso_tarjetas
```

### 7. Make Audit Rule Permanent

```bash
sudo nano /etc/audit/rules.d/monitor.rules
```

**File content:**
```
-w /home/osboxes/Documents/tarjetas_bancarias.txt -p r -k acceso_tarjetas
```

```bash
sudo augenrules --load
sudo systemctl restart auditd
sudo auditctl -l  # Verify rule
```

### 8. Set Up Gmail

- Go to: https://myaccount.google.com/security  
- Create an App Password: https://myaccount.google.com/apppasswords  
- Name: `monitor_tarjetas`  
- Copy the generated key (e.g., `grkyy nyhf uxec iing`)

### 9. Edit Script with App Password

```bash
sudo nano monitor_tarjetas.py
```

### 10. Save Script Securely

```bash
sudo mkdir -p /opt/monitor_archivo
sudo cp monitor_tarjetas.py /opt/monitor_archivo/
sudo chmod 700 /opt/monitor_archivo/monitor_tarjetas.py
sudo chown root:root /opt/monitor_archivo/monitor_tarjetas.py
```

### 11. Turn Script Into a systemd Service

```bash
sudo nano /etc/systemd/system/monitor_tarjetas.service
```

**Service content:**
```ini
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
```

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable monitor_tarjetas.service
sudo systemctl start monitor_tarjetas.service
```

### 12. Verify Service Status

```bash
sudo systemctl status monitor_tarjetas.service
```

---

## Contributing

So you want to help? That’s adorable.

1. Fork the repo  
2. Create your feature branch  
   ```bash
   git checkout -b feature/YourAmazingFeature
   ```
3. Commit your changes  
   ```bash
   git commit -m "Add something marginally useful"
   ```
4. Push to your branch  
   ```bash
   git push origin feature/YourAmazingFeature
   ```
5. Open a pull request and try to sound humble 😅

Pull requests are welcome, but they will be judged. Brutally.

---

## Roadmap

Here’s what we pretend to do, assuming we don’t get distracted:

- [ ] Web interface for monitoring logs  
- [ ] Email notifications for alerts  
- [ ] Cross-platform support (Windows & macOS)  
- [ ] Integration with cloud storage for secure backup  
- [ ] GUI installer for people who fear the terminal  

*Feel free to submit feature requests disguised as issues.*

---

## License

MIT © [Tu Nombre o Usuario]
