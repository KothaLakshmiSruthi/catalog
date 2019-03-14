# Item Catalog project Web Application
By KOTHA LAKSHMI SRUTHI
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates book categories and their editions. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## In This Project
This project has one main Python module `main_item.py` which runs the Flask application. A SQL database is created using the `db_structure.py` module and you can populate the database with test data using `initial_db.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
7. JavaScript

## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests

7. Setup application database `python /item_catalog/db_structure.py`
	db_structure.py contains the:
		* 3 table names - which are used to create users,carbrands,cardetails
		
8. *Insert sample data `python /item_catalog/initial_db.py`
	initial_db contains the sample data for some of the carbrands and cardetails
	
9. Run application using `python /item_catalog/main_item.py`
	main_item.py contains the all the html files which are used to 
		* add car brands
		* edit car brands
		* delete car brands
		* add car details
		* edit car details
		* delete car details and so on to their requirement
10. Access the application locally using http://localhost:2222

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'car store'
7. Authorized JavaScript origins = 'http://localhost:2222'
8. Authorized redirect URIs = 'http://localhost:2222/login' && 'http://localhost:2222/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in item_catalog directory that you cloned from here
14. Run application using `python /item_catalog/main.py`

##steps to be followed to run the main file(main_item.py)

1.open the command prompt in current file
2.use the command venv/scripts/activate for the activation
3.run the main file
	```main_item.py```
4.error occures ```no module found```
	and asked to install some modules
5.pip install module_name
	```pip install flask```
	```pip install 	sqlalchemy```
	```pip install requests```
	```pip install oauth2client```
6.after installing all the above modules again run the python file(main_item.py)
	```main_item.py```


## JSON Endpoints
The following are open to the public:

cars Catalog JSON: `localhost:2222/CarClub/JSON`
    - Displays the whole cars models catalog. car Categories and all models.

car Categories JSON: `localhost:2222/carClub/carCategory/JSON`
    - Displays all car brands
	
All car Editions: `localhost:2222/carClub/cars/JSON`
	- Displays all car details

car Edition JSON: `localhost:2222/carClub/<path:car_name>/cars/JSON`
	- <path:car_name> --->  give the name of particular car brand name that you require
    - Displays car models for a specific car category

car Category Edition JSON: `localhost:2222/carClub/<path:car_name>/<path:edition_name>/JSON`
    - <path:car_name> --->  give the name of particular car brand name that you require
	- <path:edition_name> --->  give the name of car that is required
	   Based on the above details given you can Displays a specific car category Model.
