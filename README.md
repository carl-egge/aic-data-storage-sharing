# Advanced Internet Computing :: Project_B1

> An end-to-end encrypted data storage and sharing system using Raspberry Pi's. Part of the Project Based Learning module of the Advanced Internet Computing course, SoSe, 2023.

## Group B1

- Ahmad Hawat (@cld0736) - Ahmad.hawat@tuhh.de
- Carl Egge (@cox5071) - carl.egge@tuhh.de
- Ghislain Nkamdjin Njike (@ciw0490) - ghislain.nkamdjin.njike@tuhh.de
- Mohammad Rayhanur Rahman (@ckf8282) - mohammad.rayhanur.rahman@nithh.de

**Team Coordinator:**

Mohammad Rayhanur Rahman

Email: mohammad.rayhanur.rahman@nithh.de

## Getting Started

> Instructions on how to use the project

### Virtual Environment

In order to run the project a few python packages are needed we want to use a virtual environment for that.
Make sure you have python and pip installed and then run:

```bash
pip install virtualenv
```

Next, we create the virtual environment for the project, launch it and install our requirements:

```bash
virtualenv <my_env_name>
source <my_env_name>/bin/activate
pip install -r requirements.txt
```

### IAM Authentication to GCP

In order to connect to the Google Cloud SQL Service we need to authenticate the process using either the gcloud SDK tools and the user credentials of the Google account or the generate a service account key with the SQL Client priviledge and store the keypath in the local environment.

### Database Credentials

For security reasons the credentials for the GCP SQL instance are stored in a local enviroment file (.env) that is not in this GitLab repository.
Without the credentials from the .env file it is not possible to connect to the SQL instance.
