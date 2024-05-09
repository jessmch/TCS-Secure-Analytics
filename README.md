# TCS-Secure-Analytics

Our confidential computing machine takes in a bank fraud dataset and builds a machine learning model off of it. With this machine learning model, our generative AI can analyze and respond to queries by the users inquiring about possible fraudulent credit card transactions.

# Setting up:

Since we are using Google Cloud and Amazon Web Services, we need to account for the differences in both systems.

## Installing Python and PIP:
### On Google Cloud
Installing Python
```
sudo apt update
sudo apt install python3 python3-dev python3-venv
```
Installing PIP
```
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```
In case the above doesn't work, you can always run pip using these commands
```
python3 -m venv .venv
source .venv/bin/activate
```
Then run this to install
`python3 -m pip install [what you want to install here]`

### On AWS
Installing Python
```
sudo yum -y update
sudo yum -y install python3
```
Installing PIP
```
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py 
```

## Installing the Required Libraries
### Cryptopgrahy
`pip install cryptography`
### Pandas
```
pip install pandas
pip install pandasai
```
### Langchain
```
pip install langchain
```
### Ollamas
```
curl -fsSL https://ollama.com/install.sh | sh
ollamas pull mistral
```
To run the mistral model, run
`ollamas run mistral`
