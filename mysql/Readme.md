
# How to run this sample code

## Requirements
You need to set the following environment variables with your data.

- HOST
- DATABASE
- USER
- PASSWORD

## Flask App
1. Create a virtual environment with any python version >=3.
    - If you are using Windows:
        ```shell
            python -m venv env
        ```
    - If you are using Linux:
        ```shell
            python3 -m venv env
       ```
2. Activate the virtual environment.
    - If you are using Windows in cmd:
        ```shell
            env\Scripts\activate.bat
        ```
    - If you are using Linux
        ```shell
            source env/bin/activate
        ```
3. Once the virtual environment is activated, install **requirements.txt**.
    ```shell
        pip install -r requirements.txt
    ```
4. Run the application.
    - If you are using Windows:
        ```shell
            python index.py
        ```
    - If you are using Linux:
        ```shell
            python3 index.py
        ```
    > The application will be listening by default on **http://127.0.0.1:5000/**


