# Northcoders Data Engineering Bootcamp: Capstone Project

## An ETL Pipeline for the fictional company 'Terrific Totes'  

We built this application as a capstone for our coursework on the Northcoders Data/Cloud Engineering bootcamp, to gain practical experience creating an ETL pipeline from the ground up and as a demonstration of the skills we learned during the 13-week course. 


Using infrastructure as code to deploy a monitored system to AWS, this application first extracts constantly updating data from a live operational database. Using lambda functions, it then stores the data in an S3 bucket and transforms it into organised Parquet format. Within 30 minutes of appearing in the original database, the processed data is loaded into a data warehouse, ready for visualisation with PowerBI, Tableau, or similar tools. 

## Tech Stack

**Technologies used**

* Python 3.12.6
* AWS (Amazon Web Services)
* Terraform
* PostgreSQL
* PG8000
* Pandas
* PyArrow
* Github Actions

The lambda functions are written in Python, using PG8000 to connect to PostgreSQL databases. The application is then deployed to AWS using Terraform and Github Actions. Our code is fully tested, and the project conforms to PEP8 standards.
## Installation

**System requirements**

* An AWS account with appropriate credentials

**Instructions**

* Clone the repository
* Enter the repository and ensure you are working within the correct directory (the folder is named 'terrific-totes-data-pipeline')
* When you have successfully cloned and entered the repo, enter the following commands to the terminal. Press enter after each one and allow the program to run until ready for the next command.

        make requirements
        make dev-setup
        make run-checks

* To initialise Terraform, first change directory to 'terraform' to enter the terraform folder of the repository. The correct path is ~/terrific-totes-data-pipeline/terraform. 
* Enter the following command:
    
        terraform init

* If Terraform successfully initialised, now enter

        terraform plan

* Finally, enter 

        terraform apply

    and type 'yes' when prompted. This deploys the code on AWS.

### Acknowledgements

Many thanks to our Northcoders 'product owner' Paul Copley for his guidance during the build phase of this project. 


## Authors

* Max Downer ([@MaxDowner](https://github.com/MaxDowner))
* Georgina Hardcastle ([@xandriska](https://github.com/xandriska))
* Charlotte Hooson ([@CharlotteHooson](https://github.com/CharlotteHooson))
* Morgan Lamb ([@CoachLamb92](https://github.com/CoachLamb92))
* Andrew Rudge ([@AndrewFudge](https://github.com/AndrewFudge))
* Hamzah Saeid ([@hamzahsaeid](https://github.com/hamzahsaeid))

## Badges


![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)

![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

![Static Badge](https://img.shields.io/badge/test%20coverage-over%2090%20percent-green)
