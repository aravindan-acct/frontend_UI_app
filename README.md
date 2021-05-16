# Introduction

This application acts as the frontend web tier to the petstore application available at: https://github.com/aravindan-acct/petstore

## Deployment options:
1. Independent deployment: To deploy the application as a standalone server, the following needs to be done on the instance/server:

    Create environment variables:

    a. `export publicip=<public ip of the server>`

    b. `export apiserver=<ip of the backend petstore api server>`

    c. Start the web server:

        `cd frontend_UI_app`
        
        `python3 -m project`

2. Deployment with an upstream Barracuda WAF. This option assumes that a Barracuda WAF instance has already been deployed as the upstream waf:
    
    Create environment variables and 'touch' a file:

    a. `export WAFIP=<private ip of the waf>`
        
        Note: This is also the ip on which the api server can be accessed  through the waf

    b. `export WAFPublicIP=<public ip of the waf>`

    c. `touch /tmp/withwaf.txt`  - This file is checked during the server initialization.


## Important Note

Please note that the 2nd deployment option is best used with the following repos.These above repos provide templates to provision the entire setup for a lab environment with barracuda waf and petstore:

1. AWS deployment: `https://github.com/aravindan-acct/awsdevdays_sep2020`

2. Azure Deployment: `https://github.com/aravindan-acct/api_sec_training_Azure_2021`

