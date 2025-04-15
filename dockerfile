# Étape 1 : Choisir une image de base
FROM debian:bullseye

# Étape 2 : Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    git \
    nmap \
    python3-pip \
    netcat \
    perl \
    perl-net-ssleay \
    && apt-get clean

# Étape 3 : Installer les dépendances pour le backend
RUN pip3 install flask

# Clone du dépôt de Photon
RUN git clone https://github.com/s0md3v/Photon.git /opt/photon
RUN pip install -r /opt/photon/requirements.txt

RUN git clone https://github.com/sullo/nikto /opt/nikto

# Étape 4 : Ajouter le code backend et frontend
WORKDIR /app
COPY backend/backend.py /app/
COPY static /app/static

# Étape 5 : Exposer le port pour l'interface web
EXPOSE 8080

# Étape 6 : Commande de démarrage
CMD ["python3", "backend.py"]
