# Initialise VM, install git, Python3, Python3 packages
#
# Before we initialise, we need to run the following code in the new VM

# yes | sudo apt update
# sudo apt-get -y -qq install git

###########
#!/bin/bash

yes | sudo apt update
yes | sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
sudo apt-get install unzip
yes | sudo apt install python3-pip
pip3 install numpy pandas sqlalchemy tqdm fredapi
yes | sudo apt-get install mysql-client
yes | sudo apt-get update
mkdir FinalProject
cd ./FinalProject
# Copies files loaded from Github to GCP Bucket
# gsutil rsync -x "\.git.*" ~/beer-sales-economy gs://depa-bucket-of-white-claws/beer-sales-economy
git clone https://github.com/benedictau1993/beer-sales-economy .
gsutil cp gs://depa-bucket-of-white-claws/IRI_beer_dataset_Au.zip .
unzip IRI_beer_dataset_Au.zip -d .
mysql --host=10.1.224.3 --user=root --password

# Copies files loaded from Github to GCP Bucket
# gsutil rsync -x "\.git.*" ~/beer-sales-economy gs://depa-bucket-of-white-claws/beer-sales-economy

# sudo shutdown
