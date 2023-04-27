# Selecto

Selecto is a Python webproject which makes it easy to filter and search for various products online. With enhanced filtering, we can find the best product for you!


# Getting Started
This project is built using tox. This allows us to build in both Unix and Windows enviroments. To run tox, please follow the below instructions:

## Environment Variables
We current have two files: `web/selecto/resources/dev.env` and ` web/selecto/resources/prod.env` which are used to store credentials.
Please use the `web/selecto/resources/template.env` file as an example to produce these two files.
Ask the other team members for our creds. We need to use these for testing and deployment for our app.

## Setup virtual environment
Here is an example on using venv.
1. Please up the terminal and naviate to the project root directory. Then run this command to setup your venv environment.
    ```
    python -m venv venv
    ```
2. If you are on **WINDOWS** please run this to activate this venv environment.
    ```
    venv\Scripts\activate     # On Windows
    ```
    If you are on **MACOS/UNIX** please run this to activate this venv environment.
    ```
    source venv/bin/activate  # On macOS/Linux
    ```

## Using Tox
1. Ensure that you have Python and pip installed on your system. If you don't have them installed, download Python from the official website (https://www.python.org/downloads/) and follow the installation instructions for your operating system.
2. Install tox using pip:
    ```
    pip install tox
    ```
3. Run the commands specified in the tox.ini file using the following syntax:
    ```
    tox -e <command>
    ```
    Replace <command> with the desired command from the tox.ini file, such as run, migrate, install, test, or init_db.

## Initalize DB
1. Run the commands 
    ```
    tox -e install
    tox -e init_db
    ```
    This will initalize the db so that you can run the server.

## Run server
1. To run the server, please use 
    ```
    tox -e run
    ```
