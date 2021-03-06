# Introduction
The full set of Turnkey Admin APIs available through a REST interface. This was originally the CloudFS quickstart guide merely demoing user and authenticate APIs. Later expanded to include the Admin APIs such as AccountState, Create and Delete

This API was built and tested on Python 2.7.5

# Installation
1. virtualenv / virtualenvwrapper

    Install [virtualenv], [virtualenvwrapper] and configure a virtual enviorenment for the application.

    ```
    $ mkvirtualenv projectname
    $ workon projectname
    ```

2. Get the source

    Clone the repository to your work space.

    ```
    $ cd /path/to/your/workspace
    $ git clone https://github.com/iispokon/cfs-admin-api.git projectname
    $ cd projectname
    ```

3. Install the required plugins

    Source folder contains a folder named 'requirements' with a file prod.txt which contains all the dependencies.

    ```
    $ cd requirements
    $ pip install -r prod.txt
    ```

    If you are not on a virtual environment run the above command with sudo.

    ```
    $ cd requirements
    $ sudo pip install -r prod.txt
    ```
    

4. Create a simlink for settings file.

    ```
    cd signup/settings
    ln -s prod.py local.py
    ```

5. Set host/domain names Django API can serve.

    Open settings/common.py and update ALLOWED_HOSTS to host or domain name.
    ALLOWED_HOSTS = ['127.0.0.1']


6. Edit configuration

    Edit the below configurations in settings/common.py with API endpoint, Client ID, Client secret, Admin Id and Admin secret data obtained from Bitcasa account to enable user creation and authentication feature. If you do not hold admin related details that is only available for paid account users, please leave the values blank.

    ```
    api_server = {'cfs': 'xxxx.cloudfs.io'}
    client_id = {'cfs': 'xxxxxx'}
    secret_key = {'cfs': 'xxxxxxxxxxxxx'}
    admin_id = {'cfs': 'xxxxxx'}
    admin_secret = {'cfs': 'xxxxxxxxxxxxx'}
    ```

7. Run the project

    Go to the project root folder in a command shell and run the below command

    ```
    python manage.py runserver
    ```

    Check urls http://127.0.0.1:8000/api/user/, 
    http://127.0.0.1:8000/api/authenticate/, 
    http://127.0.0.1:8000/api/accountState/, 
    http://127.0.0.1:8000/api/create/, 
    http://127.0.0.1:8000/api/delete/


# API
The API contains the following end points
####User
End point for creating a user.

```
<hostname>/api/user/
```

Need to send a post request with below parameters.
* username	- The username for the new user
* password	- The password for the new user
* first_name	- The first name for the new user
* last_name	- The last name for the new user

If the user is created successfully server will send a response with http status code 201. Else server will send a response with status code 400 with a message in the body.

Response parameters.
* success - True, False indicating whether the user creation is success or failure
* message - The detail message

####Authenticate
End point for retrieving auth token.
```
<hostname>/api/authenticate/
```

Need to send post request with below paremeters.
* username	- Username for your account
* password	- Password for your account

If the request is successfull server will send a response with http status code 200 and auth_token in the body. Else server will send a response with status code 400 and message in the body.

Response parameters.
* auth_token - The authrorization token if the request is successfull
* success - True, False indicating whether the token generation is success or failure
* message - The detail message


####AccountState
```
<hostname>/api/accountState/
```
Documentation available from your Bitcasa SA or Sales Rep

####Create
```
<hostname>/api/create/
```
Documentation available from your Bitcasa SA or Sales Rep

####Delete
```
<hostname>/api/delete/
```
Documentation available from your Bitcasa SA or Sales Rep


[virtualenv]:http://virtualenv.readthedocs.org/en/latest/virtualenv.html
[virtualenvwrapper]:http://virtualenvwrapper.readthedocs.org/en/latest/install.html
