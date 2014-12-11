# Introduction
CloudFS user signup REST API provide end points for user creation and authentication.

# Installation
1. virtualenv / virtualenvwrapper
    Install [virtualenv], [virtualenvwrapper] and configure a virtual enviorenment for the application.

    ```
    $ mkvirtualenv projectname
    ```

2. Get the source
    Clone the repository to your work space.

    ```
    $ git clone [git-repo-url] projectname
    ```

3. Install the required plugins
    Source folder contains a folder named 'required' with a file prod.txt which contains all the dependencies.

    ```
    $ workon projectname
    $ cd projectname/requirements
    $ pip install -r prod.txt
    ```

4. Create a simlink for settings file.

    ```
    cd signup/settings
    ln -s prod.py local.py
    ```

5. Edit configuration
    Edit the below configurations in settings/common.py with your account data.

    ```
    CLOUD_FS_SETTINGS = {
        'API_SERVER': 'xxxxx.cloudfs.io',  
        'CLIENT_ID': 'xxxxxxxxxx',  
        'SECRET_KEY': 'xxxxxxxxxxxxxxxxxxxxxxxxxx',  
        'ADMIN_ID': 'xxxxxxxxx',  
        'ADMIN_SECRET': 'xxxxxxx'  
    }
    ```

6. Run the project
    Go to the project root folder in a command shell and run the below command

    ```
    python manage.py runserver
    ```

    Check urls localhost/api/user/, localhost/api/authenticate/


# API
The API contains two end points
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

[virtualenv]:http://virtualenv.readthedocs.org/en/latest/virtualenv.html
[virtualenvwrapper]:http://virtualenvwrapper.readthedocs.org/en/latest/install.html
