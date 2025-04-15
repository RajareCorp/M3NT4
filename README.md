 ██▀███   ▄▄▄      ▄▄▄██▀▀▀▄▄▄       ██▀███  ▓█████ <br>
▓██ ▒ ██▒▒████▄      ▒██  ▒████▄    ▓██ ▒ ██▒▓█   ▀ <br>
▓██ ░▄█ ▒▒██  ▀█▄    ░██  ▒██  ▀█▄  ▓██ ░▄█ ▒▒███   <br>
▒██▀▀█▄  ░██▄▄▄▄██▓██▄██▓ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄ <br>
░██▓ ▒██▒ ▓█   ▓██▒▓███▒   ▓█   ▓██▒░██▓ ▒██▒░▒████▒<br>
░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒▒░   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░<br>
  ░▒ ░ ▒░  ▒   ▒▒ ░▒ ░▒░    ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░<br>
  ░░   ░   ░   ▒   ░ ░ ░    ░   ▒     ░░   ░    ░   <br>
   ░           ░  ░░   ░        ░  ░   ░        ░  ░<br>


This project provides a secure environment for running a web application behind a VPN and Tor. It includes tools like Photon and Nikto for penetration testing, Flask for backend services, and DNS anonymization.

---

## Features

- **VPN Integration:** Protect all outgoing traffic using OpenVPN.
- **Tor Configuration:** Additional layer of anonymity for internet connections.
- **Penetration Testing Tools:**
  - [Photon](https://github.com/s0md3v/Photon) for crawling and scraping.
  - [Nikto](https://github.com/sullo/nikto) for web server scanning.
- **Backend Framework:** Flask for running the web application.
- **DNS Privacy:** Routes all DNS requests through privacy-focused DNS servers.

---

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- A valid `.ovpn` configuration file from your VPN provider.

---

## Installation and Usage

### Step 1: Clone the Repository
```bash
git clone https://github.com/RajareCorp/M3NT4.git
cd your-repo-name
```
### Step 2: Provide VPN Configuration
Place your .ovpn file in the vpn-config directory. Ensure it matches your preferred server and authentication method.

### Step 3: Build the Docker Image
Build the Docker image using the following command:

```bash
docker build -t secure-app .
```
### Step 4: Run the Application
Run the Docker container:
```bash
docker run --cap-add=NET_ADMIN --device /dev/net/tun -p 8080:8080 secure-app
```
The application will be accessible at http://localhost:8080.