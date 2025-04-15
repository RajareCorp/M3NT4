FROM debian:bullseye

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    git \
    nmap \
    python3-pip \
    netcat \
    perl \
    perl-net-ssleay \
    tor \
    openvpn \
    curl \
    iproute2 \
    resolvconf \
    && apt-get clean

# Configurer et démarrer le service Tor
RUN service tor start

# Installer les dépendances pour le backend
RUN pip3 install flask

# Installer Photon
RUN git clone https://github.com/s0md3v/Photon.git /opt/photon
RUN pip install -r /opt/photon/requirements.txt

# Installer Nikto
RUN git clone https://github.com/sullo/nikto /opt/nikto

# Ajouter le fichier de configuration OpenVPN (assurez-vous de fournir votre fichier .ovpn)
COPY ./vpn-config /etc/openvpn

# Modifier le fichier resolv.conf pour inclure des DNS anonymes
RUN echo "nameserver 1.1.1.1" >> /etc/resolv.conf && \
    echo "nameserver 9.9.9.9" >> /etc/resolv.conf

# Ajouter le code backend et frontend
WORKDIR /app
COPY backend/backend.py /app/
COPY static /app/static

# Exposer le port pour l'interface web
EXPOSE 8080

# Commande de démarrage avec connexion au VPN
CMD openvpn --config /etc/openvpn/config.ovpn & python3 backend.py
