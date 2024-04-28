# Getting Started to Run MovieMatch Application

This project created using React and Flask
To Run this Project, please follow the steps below.

# Prerequisites required
Python 3.9 should be install
pip should be installed

# Create a New Virtual Enviroment using Conda (Optional)
conda create -n myenv python=3.9

# Activate th Enviroment to install dependenices (Optional)
conda activate myenv

# Install the dependencies using requirements.txt
pip install -r requirements.txt

# Setting up Enviroment Variables (if not present when uncompressed)
From the env.txt, copy all of the contents of it.
Create a file as '.env'
Paste the contents into created file

# Run the Main App (Linux and Mac Users Only)

(NOTE: make sure nothing running on the port 8080
if the port is occupied  in app.py line 414 change the port number if necessary)

python app.py

# Running the Main App (Windows Users)

Please replace line 414 in app.py as below to run development server provided by flask
(NOTE: make sure nothing running on the port 8080
if the port is occupied  in app.py line 414 change the port number if necessary)
app.run(port=8080)

then do
python app.py

# Run the Tests
python -m unittest tests.py

# This application is already deployed using openshift
https://mm-moviematch.apps.a.comp-teach.qmul.ac.uk


