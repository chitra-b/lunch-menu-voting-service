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
