# COMP9900 PROJECT
# capstone-project-runtime-terror

Intelligent Assistant for electronic Logbook in Radiology training

# Web App Install
1. Create local version of python (virtualenv).
```
virtualenv -p python3 env
```
2. Activate virtualenv.
```
source env/bin/activate
```
3. Install required modules.
```
pip install -r requirements.txt
```
4. Install a local database and initialize with an in-built 'Admin account'
(NOTE: This step only needs to be done in the very first instance)
```
python3 db_create.py
python3 db_populate.py
```
5. Good to go! Run the server.
```
python3 run.py
```
6. To deactivate the virtual env
```
deactivate
```



# Chatbot Install
1. Open a new terminal and go to the directory /capstone-project-runtime-terror-master/chatbot, then input:
```
npm install -g localtunnel
```
2. Open a new terminal and go to the directory /capstone-project-runtime-terror-master/chatbot, then input:
```
pip3 install -r requirements.txt
```
3. Open a new terminal and go to the directory /capstone-project-runtime-terror-master/chatbot/app13/demo, then input:
```
python3 __init__.py
```
4. Open a new terminal and go to the directory  /capstone-project-runtime-terror-master/chatbot/, then input:
```
python3 app.py
```
5. After that, please open a new terminal and input:
```
lt --port 5000 --subdomain 9900chatbot2
```


