# address-book

This repository contains a FastAPI project for building an address book application - a simple yet powerful tool for managing addresses. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have Python 3.7 or later installed on your system. You can download it from the official Python website: Python Downloads

### Installation

Clone the repository:
```bash
git clone https://github.com/vaseemrajakottarath/address-book.git
```
Navigate to the project directory

Install the dependencies:

```bash
pip install -r requirements.txt
```
### Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
### Usage

The API server should now be running locally at http://localhost:8000.

Once the server is running, you can access the API endpoints using tools like cURL, Postman, or your web browser. Here are the endpoints:

/addresses/ : Create a new  address with lat and long created of the address.

/all_addresses/ : Get all address details.

/addresses/{address_id} : Get address by id.

/addresses/nearby/ : Get address within distance,latitude and longitude.

/addresses/{address_id} : Update the address by id.

/delete_address/{address_id} : Delete the address by id.

For detailed API documentation and interactive testing, visit http://localhost:8000/docs.

### Acknowledgments

FastAPI Documentation

Python Requests

UVicorn Documentation
