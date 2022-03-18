# Dev

> copier le repertoire sur le raspberry

    scp gpio-relay/* cncjs.local:/home/pi/gpio-relay
    
# Installation

    apt-get install -y python3-pip
    pip3 install "poetry==1.1"
    poetry update

# Run

    poetry run python main.py
