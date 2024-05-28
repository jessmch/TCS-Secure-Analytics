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

If the permission is denied while running the memory dump script, run `chmod +x mem_dump_aws.sh` and `chdmod +x mem_dump_gc.sh`

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
sudo vim /etc/nitro_enclaves/allocator.yaml
sudo systemctl restart nitro-enclaves-allocator.service
```
Change memory_mib to `9000`
Allocate Resources to the Enclave
`sudo systemctl enable --now nitro-enclaves-allocator.service`
You may check this file to change the default allocation settings
`/etc/nitro_enclaves/allocator.yaml`
Start the Docker service and make sure it runs every time the instance starts up
`sudo systemctl enable --now docker`
#### Setting up the Enclave
Go to the program's directory
`cd TCS-Secure-Analytics`
In the directory to create a Docker image run
`sudo docker build -t tcs-black-box .`
To test if it runs, run this docker command
`sudo docker run --rm -it -v ollama:/root/.ollama tcs-black-box`
Build the enclave file
`sudo nitro-cli build-enclave --docker-uri tcs-black-box:latest --output-file tcs-black-box.eif`

The below steps are not necessary, but useful if you want to make sure that the enclave runs properly

Run the enclave file
`sudo nitro-cli run-enclave --cpu-count 2 --memory 9000 --enclave-cid 16 --eif-path tcs-black-box.eif --debug-mode`
To check running enclaves
`nitro-cli describe-enclaves`
Since we ran the enclave in debug mode, we can check its output using
`nitro-cli console --enclave-id <ENCLAVE ID HERE>`
To terminate the running enclave
`nitro-cli terminate-enclave --enclave-id <ENCLAVE ID HERE>`


### Extra Notes
To remove all Docker images, run
`docker image prune`
`docker container prune`
`docker builder prune`

### For completely wiping out docker space in AWS
Continually remaking the docker image will cause extra data to take up space. Please remember to wipe it out if this is the only docker image you are using
```
docker system prune --all
sudo rm -r /var/lib/docker/overlay2/
sudo rm -r /var/lib/docker/image
sudo rm -r /var/lib/docker/devicemapper
sudo systemctl restart docker
```

# Running the program
In both the Google Cloud and AWS instaces, clone the Github repository
## In Google Cloud
1. Go to the program's directory 
`cd TCS-Secure-Analytics`
2. Use TMUX to split the terminal in two (Run `tmux`, then use Ctrl+B and then %) 
3. In one terminal, run the main program
`python3 main.py`
4. In the other terminal, continue to run the memory dump attack at multiple points during the main program's execution
`./mem_dump_gc.sh`

Results from the memory dump attack show how vulnerable the data is currently

## In AWS
1. Go to the program's directory 
`cd TCS-Secure-Analytics`
2. Use TMUX to split the terminal in two (Run `tmux`, then use Ctrl+B and then %)
3. In one terminal, run the Enclave file
`sudo nitro-cli run-enclave --cpu-count 2 --memory 9000 --enclave-cid 16 --eif-path tcs-black-box.eif --debug-mode`
Optional: To see what the enclave is outputting, use the enclave ID returned from the command above in this command
`nitro-cli console --enclave-id <ENCLAVE ID HERE>`
4. In the other terminal, run the memory dump attack
```
chmod +x mem_dump_aws.sh
./mem_dump_aws.sh
```

The constant message that there is no associated memdump.core file is proof that the data in the enclave is secure from outside interference


The program will automatically terminate in 5 minutes after the response time