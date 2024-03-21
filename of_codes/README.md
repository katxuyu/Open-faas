https://www.openfaas.com/blog/openfaas-flask/
https://github.com/openfaas/python-flask-template
Create openfaas-flask codes:
 - faas-cli template store pull python3-http
 - faas-cli new --lang python3-http $FN

 logs:
 faas-cli logs inmarsat --gateway=http://20.188.114.120:8080


 to add consumer group:
 - download apache kafka binary
 - install Java 
 - https://www.conduktor.io/kafka/kafka-consumers-in-group-cli-tutorial/



install pipenv then run 
    - pipenv install flask
    - pipenv install kafka-python

To run the receive-produce.py (script for receiving message from webhook and feeding to kafka)
    - run shell script
        - ./runrp.sh

To run consume-post.py (script for consuming message from kafka and posting to API)
    - python3 consume-post.py


Request Headers
Authorization: Bearer 
Content-Type: application/json


install/deploy openfaas:
    git clone https://github.com/openfaas/faasd --depth=1
    cd faasd
    ./hack/install.sh

Deploy:
faas-cli up -f flask-service.yml

Deploying image to docker:
1. build the image first: 
    sudo -E faas-cli build -f receive-produce.yml
2. check if image exist: 
    sudo -E docker images
3. Create an account to Hocker Hub 
4. login to docker account using cli: 
    sudo -E docker login -giegrajo
    dckr_pat_8VGodDU8bS4gDE50q17NRnRwihc
5. If error create docker user:
    sudo -E groupadd docker
    sudo -E usermod -aG docker ${USER}
    sudo -E usermod -a -G docker $USER
5. If successful:
    sudo -E docker tag giegrajo/receive-produce:latest giegrajo/receive-produce:latest
6. push image to docker:
    sudo -E docker push giegrajo/receive-produce:latest


Deploying code to faas
1. login to faas server: 
    sudo -E faas-cli login -g http://20.188.114.120:8080/ -p WuCKS4vNVa0GmfX0G0b4VTZGeOkTGZAFCr0ec7kHVZebf6lKA5sy9pXQQTWAtqN
2. sudo -E faas-cli push -f receive-produce.yml
3. sudo -E faas-cli deploy -f receive-produce.yml --gateway=http://20.188.114.120:8080/

Deploying with image:
    sudo -E docker login
    sudo -E docker pull giegrajo/receive-produce:latest
    NOTE: MAKE THE DOCKER REPOSITORY PUBLIC IN DOCKER HUB
    sudo -E faas-cli deploy --image giegrajo/receive-produce --name receive-produce --gateway=http://20.188.114.120:8080/

faas-cli login -g http://20.188.114.120:8080 -p WuCKS4vNVa0GmfX0G0b4VTZGeOkTGZAFCr0ec7kHVZebf6lKA5sy9pXQQTWAtqN