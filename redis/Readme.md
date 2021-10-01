
# How to run this sample code

## Create an Azure Redis Cache database
1. Navigate to the Azure Portal https://portal.azure.com/#create/Microsoft.Cache to create a Redis Cache database.
2. Select or create a new `Resource Group`.
3. Enter a DNS Name:  **`<name>.redis.cache.windows.net.`**
4. Select a **Location**.
5. Choose Basic C0 (250 MB Cache) for Pricing Tier.
6. Unblock port `6379` checkbox and press on `Create`.
7. Navigate under `Settings` to `Access Keys` and copy the `Primary Key`, which will be used as Password.
8. Navigate under `Settings` to `Properties` and copy `Host Name` value, which will be used as Host.

## Set Environment variables
You need to set the following environment variables with the previous data from Azure Redis Cache.

- HOST
- PASSWORD

For Windows: `set HOST=<alias>.redis.cache.windows.net` and the same for password.

For Linux: `export HOST=<alias>.redis.cache.windows.net` and the same for password.


## Flask App
1. Clone this repository with **`git clone https://github.com/azureossd/python-databases-samples.git`**.
2. Cd into **python-databases-samples/redis** directory.
3. Create a virtual environment with any python version >=3.
    - If you are using Windows:
        ```shell
            python -m venv env
        ```
    - If you are using Linux:
        ```shell
            python3 -m venv env
       ```
4. Activate the virtual environment.
    - If you are using Windows in cmd:
        ```shell
            env\Scripts\activate.bat
        ```
    - If you are using Linux
        ```shell
            source env/bin/activate
        ```
5. Once the virtual environment is activated, install **requirements.txt**.
    ```shell
        pip install -r requirements.txt
    ```
6. Run the application.
    - If you are using Windows:
        ```shell
            python index.py
        ```
    - If you are using Linux:
        ```shell
            python3 index.py
        ```
    
    > The application will be listening by default on **http://127.0.0.1:5000/**

## Deploy to Azure App Service Linux
1. Create a new Azure Web App Python Linux from the Azure Portal (preferably with Python 3.8 or latest) to deploy to Azure.
2. Set up **Local Git** and copy your local git url.
3. Click on **Configuration** and create the App Settings HOST,PASSWORD with the same values.
4. Run the following commands to deploy:
   ```bash
      git init
      git add .
      git commit -m "Initial Commit to Azure"
      git remote add azure https://<sitename>.scm.azurewebsites.net:443/<sitename>.git
      git push azure master
   ```
5. Browse to the site **https://<sitename>.azurewebsites.net/** to review all operations for this application.