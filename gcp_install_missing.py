
# Install Missing Packages

#!/bin/bash

sudo apt-get update
sudo apt-get -y -qq --fix-missing install python3-os python3-glob python3-numpy python3-pandas python3-sqlalchemy python3-tqdm python3-time  python3-fredapi
