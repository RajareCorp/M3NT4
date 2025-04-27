FROM debian:bullseye

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    git \
    nmap \
    python3-pip \
    netcat \
    perl \
    libnet-ssleay-perl \
    tor \
    openvpn \
    openvpn-systemd-resolved \
    curl \
    iproute2 \
    dnsutils \
    && apt-get clean

# Installer les dépendances pour le backend
RUN pip3 install flask

# Outils

RUN git clone https://github.com/s0md3v/Photon.git /opt/photon
RUN pip install -r /opt/photon/requirements.txt
RUN pip install sherlock-project
RUN git clone https://github.com/sullo/nikto /opt/nikto

# Configurer un alias pour curl avec Tor
# RUN echo "alias torcurl='curl --socks5-hostname 127.0.0.1:9050'" >> ~/.bashrc

# Ajouter le code backend et frontend
WORKDIR /app
COPY backend/ /app/
COPY static /app/static

# Exposer le port pour l'interface web
EXPOSE 8080

# Commande de démarrage
CMD openvpn --config /etc/openvpn/config.ovpn --log /var/log/openvpn.log & python3 backend.py



