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
sudo python3 get-pip.py --break-system-packages
```
Make sure that all pip installations end with `--break-system-packages`

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
## Installing Git
### On AWS
```
sudo yum install git
```
### On Google Cloud
```
sudo apt -get install git
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
pip install langchain_experimental
```
### Ollamas
```
curl -fsSL https://ollama.com/install.sh | sh
ollamas pull mistral
```
To run the mistral model, run
`ollamas run mistral`
Then press CTRL+D to suspend the process while keeping the model running
### Retrieving the Datasets
```
pip install gdown

# fraudTest.csv
gdown 19eVy7Sb8f8j2QygAHUBRNHTA3H-EHJZl

# fraudTrain.csv
gdown 1GLpLfEzmIAUbIAIPabJpIH_Aw0PI4gHo
```
### For the memory dump attack
#### For Google Cloud
`sudo apt-get install binutils`
`sudo apt-get install gdb`
`sudo apt-get install tmux`

#### For AWS
`sudo yum install binutils`
`sudo yum install gdb`
`sudo yum install tmux`

If the permission is denied while running the memory dump script, run `chmod +x mem_dump.sh`