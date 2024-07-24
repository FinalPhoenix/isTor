# Tor Exit Node API

  

This project provides an API to check if an IP address is a Tor exit node, retrieve all Tor exit nodes, and delete specific IP addresses from the list. The project uses Flask for the API, SQLite for data storage, Docker for containerization, and Terraform for deployment on AWS.

  

## Table of Contents

  

- [Setup](#setup)

- [Running the Application](#running-the-application)

- [API Endpoints](#api-endpoints)

- [Curl Examples](#curl-examples)

- [Analysis & Implementation Review](#analysis--implementation-review)
  

## Setup

  

1.  **Clone the repository**:

  

```bash

git clone https://github.com/FinalPhoenix/isTor.git

cd isTor

```

  

2.  **Install Docker**:

  

Ensure that Docker is installed on your machine. Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker for your operating system.

  

3.  **Build and run the Docker containers**:

  

```bash

docker-compose up --build

```

  

This command will build the Docker image and start the application in a container.

  

## Running the Application

  

1.  **Access the API**:

  

Once the Docker containers are running, you can access the API at `http://localhost:5000`.


The scheduler script runs automatically in the background every 24 hours to refresh the Tor exit node list.

  

## API Endpoints

  

-  **Check if an IP is a Tor exit node**:

  

```bash

GET /ip/<ip>

```

  

-  **Get all Tor exit node IPs**:

  

```bash

GET /ips

```

  

-  **Delete an IP from the list**:

  

```bash

DELETE /ip/<ip>

```

  

## cURL Examples

  

### Check if an IP is a Tor exit node

For ease of use I've included example curl commands here to test if you don't like the swagger front end:

### Pull a list of all IP addresses stored

```bash
curl -X GET "http://localhost:5000/ips"
```

### Check if ipv4 address exists / doesn't exist

Example of a successful call with a known tor node:
```bash
curl -X GET "http://localhost:5000/ip/95.216.107.105"
```

Example of a successful call with a known not tor node

```bash

curl  -X  GET  "http://localhost:5000/ip/1.2.3.4"

```


### Check if ipv6 address exists / doesn't exist

Example of a successful call with a known tor node:
```bash
curl -X GET "http://localhost:5000/ip/2001:0db8:85a3:0000:0000:8a2e:0370:7334"
```

Example of a successful call with a known not tor node (my ip address lol)

```bash

curl  -X  GET  "http://localhost:5000/ip/2601:1c0:4400:6ff0:13a:12e9:d5a2:b9b8"

```

# Analysis & Implementation Review

Upon receiving the requirements for the project I quickly determined the key features of the application

* RESTful API
* Some database to store the txt file locally for parsing
* Documentation on how to use the API
* Docker/Terraform implementation

On initial outset, I believed that the security of dealing with a database would be the issue, but I quickly realised that it was ipv6 addresses which were going to be the hardest to work with. 

## Data Issues

The list provided was simple but unfortunately they made the decision to add brackets `[]` around ipv6 addresses which meant that some data cleaning upon ingest had to occur, I validated that the ingest list was actually ip addresses and then I stripped the ipv6 addresses of their brackets. 


## Architecture Choices

* Flask is by far the easiest to implement an API in Python and has a REST api boilerplate that we can use to set up the API quickly
* Swagger is my favorite documentation platform and integrates directly into Flask for easy set up and also will allow for testing via the web so no need to do curl requests to validate
* Since we only need to store essentially a text file, I chose sqllite for ease of use for the Proof of Concept, SQLLite has it's downsides, being a file based database it is limited in size and security controls
	* If I needed to productionalise this, I'd probably use Postgres as it has great performance
* Decided to do multithreading to allow for the scheduler to run without a cron job in docker to kick it off every 24 hours.

## How I would improve (with more time)
* As mentioned earlier SQLLite won't work if this needs to scale
* There is no auth on the API, implementing API tokens would be easy and more secure but user Authentication wasn't a requirement
* Unit Testing
