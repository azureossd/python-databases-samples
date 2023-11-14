
# How to run this sample code

## Requirements
You need to set the following environment variables with your data.

- HOST
   - If you are using SQL Azure then consider HOST=**servername**.database.windows.net and USER=**username**@**servername** in this format.
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
4. For installing **pymssql** it will vary depends on the OS.

- **Windows**: Refer to [this documentation](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-1-configure-development-environment-for-pymssql-python-development?view=sql-server-ver15#windows) to install the correct wheel file regarding your Python version and machine architecture
- Linux: Refer to [this documentation](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-1-configure-development-environment-for-pymssql-python-development?view=sql-server-ver15#ubuntu-linux), you need some previous libraries as **freetds-dev** and **freetds-bin**.
- **MacOS**: Refer to [this documentation](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-1-configure-development-environment-for-pymssql-python-development?view=sql-server-ver15#macos), you need previous library as FreeTDS.

> Note: This sample was created for  **Python Windows 3.8.2 using Win32 bits**, the wheel downloaded is **pymssql-2.1.4-cp38-cp38-win32.whl** from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
> To install and run this sample, you will need to install the wheel manually with the following command:
>```shell
>    pip install pymssql-2.1.4-cp38-cp38-win32.whl 
>```

5. Run the application.
    - If you are using Windows:
        ```shell
            python index.py
        ```
    - If you are using Linux:
        ```shell
            python3 index.py
        ```

    - You can also run via the Flask CLI:
        ```shell
            flask run
        ```

    > The application will be listening by default on **http://127.0.0.1:5000/**


