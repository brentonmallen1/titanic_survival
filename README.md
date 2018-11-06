# Titanic Survival
```
                   ,:',:`,:'
                __||_||_||_||___
           ____[""""""""""""""""]___
           \ " '''''''''''''''''''' \
    ~~jgs~^~^~^^~^~^~^~^~^~^~^~~^~^~^~^~~^~^
```

Micro service and web app created for a Meetup demo.

This repo contains everything needed to build a machine learning
model on the Kaggle [Titanic](https://www.kaggle.com/c/titanic)
dataset and implement that model as aweb app / API using AWS
API Gateway and Lambda.

The deployment process is performed using
[Zappa](https://github.com/Miserlou/Zappa).

### Use

**Web App:**

https://hvom0tv9l8.execute-api.us-east-1.amazonaws.com/dev/


**API:**

Make a POST request to the `/titanic` resource
with the following form-data:
```
    Pclass - Cabin Class - [1, 2, 3]
    Sex - [0: female, 1: male]
    Age - <Positive Integer>
    SibSp - <Positive Integer>
    Parch - <Positive Integer>
    Fare - <Float>
    Embarked - [0: Southampton, 1: Cherbourg, 2: Queenstown]
    Alone - [0: Not Alone, 1: Alone]
```
Definitions:

- **SibSp** - Number of Siblings or Spouses Aboard
- **Parch** - Number of Parents or Children Aboard
- **Fare** - Amount Paid for Ticket
- **Embarked** - Embarked Location


### Development
If you'd like to develop on this, the initial workflow was using the 
`environment.yml` file to describe a Conda environment and build the
`requirements.txt` file to build the virtualenv from there.

**Note:** The reason for two different environments is a combination of
development ease and Zapp (at the time of making this) doesn't support
conda environments.

#### Environments

**Conda**

To build the conda environment use the following from the root directory:

`conda env update` 

To extract the dependencies from the conda environment use the following 
from the root directory (Only if they need to be updated):

`make update-requirements`

**Virtualenv**

To build the virtualenv for Zappa deployment (or development if you choose)
use the following:

`make init`


### Running App Locally
The web app and api can be run locally using the flask server.  The following
can be used to start, stop and restart the flask server, respectively:

`make start`,
`make stop`,
`make restart`

**Note:** If for any reason while attempting to start the flask server you 
receive
an error stating that one is already running or the port is in use
(and `make stop` doesn't work), you can identify the running process using
`make find-pid` to find the running process for manual termination.


### Testing
To run the tests, execute the following from the root directory:

`make test`

### Model Training
To execute the model training script, use the following from the root
directory (assuming the virtualenv has been created):

`make train`

Upon completion, the script will output a model to the `models/` directory
called `titanic_model.pkl`

### Deployment
To deploy the wap/api to the web, first ensure you've
[setup](https://github.com/Miserlou/Zappa/blob/master/README.md#installation-and-configuration)
Zappa and then run the following to deploy, update and destroy the stack,
respectively:

`make deploy`,
`make redeploy`,
`make remove`

If you should see any errors, or are curious to view the AWS logs, Zappa
allows you to do this and can be done by using the following from the
root directory:

`make logs`