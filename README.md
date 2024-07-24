# Tor Exit Node API

This project provides an API to check if an IP address is a Tor exit node, retrieve all Tor exit nodes, and delete specific IP addresses from the list. The project uses Flask for the API, SQLite for data storage, Docker for containerization, and Terraform for deployment on AWS.

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Curl Examples](#curl-examples)
- [Running Tests](#running-tests)
- [Common Troubleshooting Steps](#common-troubleshooting-steps)
- [Contributing](#contributing)
- [License](#license)

## Setup

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install Docker**:

    Ensure that Docker is installed on your machine. Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker for your operating system.

3. **Build and run the Docker containers**:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image and start the application in a container.

## Running the Application

1. **Access the API**:

    Once the Docker containers are running, you can access the API at `http://localhost:5000`.

The scheduler script runs automatically in the background every 24 hours to refresh the Tor exit node list.

## API Endpoints

- **Check if an IP is a Tor exit node**:

    ```bash
    GET /ip/<ip>
    ```

- **Get all Tor exit node IPs**:

    ```bash
    GET /ips
    ```

- **Delete an IP from the list**:

    ```bash
    DELETE /ip/<ip>
    ```

## Curl Examples

### Check if an IP is a Tor exit node

#### Request

```bash
curl -X GET "http://localhost:5000/ip/1.2.3.4"