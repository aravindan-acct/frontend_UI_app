# Introduction

This application acts as the frontend web tier to the petstore application available at: https://github.com/aravindan-acct/petstore

Deployment options:
1. Independent deployment: To deploy the application as a standalone server, the following needs to be done on the instance/server:

    Create environment variables:

    a. `export publicip=<public ip of the server>`

    b. `export apiserver=<ip of the backend petstore api server>`

2. Deployment with an upstream Barracuda WAF:
    
    Create environment variables:

    a. `export WAFIP=<private ip of the waf>`
        
        Note: This is also the ip on which the api server can be accessed  through the waf

    b. `export WAFPublicIP=<public ip of the waf>`


Please note that the 2nd deployment option is best used with the following repos.These above repos provide templates to provision the entire setup for a lab environment with barracuda waf and petstore:
https://github.com/aravindan-acct/awsdevdays_sep2020
https://github.com/aravindan-acct/api_sec_training_Azure_2021

