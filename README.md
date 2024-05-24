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
sudo apt-get install git
```
## Installing the Required Libraries
### SciKit Learn
`pip install scikit-learn`
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
ollama pull mistral
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

### Setting up the Nitro Enclave
#### Download dependencies
```
sudo yum -y install aws-nitro-enclaves-cli
sudo yum -y install aws-nitro-enclaves-cli-devel
```
Set up Docker settings
```
# username is the username you used to log into the ssh
sudo usermod -aG ne username
sudo usermod -aG docker username
```
Verify the Nitro Enclave installation
`nitro-cli --version`
Change the allocation settings for all Enclaves
```
sudo chmod 777 /etc/nitro_enclaves/allocator.yaml
vim /etc/nitro_enclaves/allocator.yaml
sudo systemctl restart nitro-enclaves-allocator.service
```
Change memory_mib to `8000`
Allocate Resources to the Enclave
`sudo systemctl enable --now nitro-enclaves-allocator.service`
You may check this file to change the default allocation settings
`/etc/nitro_enclaves/allocator.yaml`
Start the Docker service and make sure it runs every time the instance starts up
`sudo systemctl enable --now docker`
#### Setting up the Enclave
In the directory to create a Docker image run
`sudo docker build -t tcs-black-box .`
Build the enclave file
`sudo nitro-cli build-enclave --docker-uri tcs-black-box:latest --output-file tcs-black-box.eif`
Run the enclave file
`sudo nitro-cli run-enclave --cpu-count 2 --memory 2428 --enclave-cid 16 --eif-path tcs-black-box.eif --debug-mode`


### Extra Notes
To remove all Docker images, run
`docker image prune`
`docker container prune`
`docker builder prune`

### For completely wiping out docker space in AWS
```
sudo systemctl stop docker
sudo yum remove docker
sudo rm -r /var/lib/docker/overlay2
sudo mkdir /var/lib/docker/overlay2
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```