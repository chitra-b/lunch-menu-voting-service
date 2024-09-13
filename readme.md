## Project Overview
Lunchmate is a backend application designed to assist employees in choosing lunch places by providing functionalities to upload daily menus, vote on menus, and view daily results. This service supports different versions of a mobile app for voting and ensures high availability and scalability.

## System Overview
### Features
* Employees can sign up and view daily menus
* Restaurant owner can sign up to upload daily menus
* The backend supports both old and new versions of the app, which affects the voting API behavior.
* Employees can vote for daily menus
* Results can be viewed for a day

### Technical Requirements
* Framework: Python with Django Rest Framework (DRF)
* Containerization: Docker

### Docker
Run the Docker compose:
* docker-compose up --build

### Testing
Run Unit Tests:
* python manage.py test

API Documentation - https://documenter.getpostman.com/view/7691096/2sAXqnfQFE



## High Availability (HA) Cloud Architecture Diagram

                         +-----------------------+
                         |      Users/Clients     |
                         +-----------+-----------+
                                     |
                                     |
                        +------------+-------------+
                        |    Azure Application      |
                        |         Gateway            |
                        +------------+-------------+
                                     |
       +-----------------------------+------------------------------+
       |                                                            |
    +------+-------+                                        +-----------+-------+
    | Azure App    |                                        | Azure App    |
    | Service      |                                        | Service      |
    | (Containerized|                                        | (Containerized|
    | Django App)  |                                        | Django App)  |
    +------+-------+                                        +-----------+-------+
       |                                                            |
       |                                                            |
    +------+-------+                                        +-----------+-------+
    | Azure Database|                                        | Azure Database|
    | for PostgreSQL |                                        | for PostgreSQL |
    | (Primary)      |                                        | (Read Replica)|
    +------+-------+                                        +-----------+-------+
       |                                                            |
       |                                                            |
       +------------+              +----------------+-------------+
                    |              |                |
                    |              |                |
       +------------+-------+   +--+------------+---+   +-----------------+
       | Azure Backup  |
       +---------------+   +-----------------+
