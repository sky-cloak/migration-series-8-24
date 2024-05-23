# Keycloak Migration Scripts

This repository contains scripts and information related to the migration of Keycloak from version 8 to version 24. The scripts include tools for generating users, setting up environments, and other utilities needed for a successful mock of a real migration.

For a comprehensive guide on the migration process, please refer to our detailed blog post: [Upgrade Keycloak from 8 to 24: A Complete Guide](https://skycloak.io/upgrade-keycloak-from-8-to-24-a-complete-guide/)

## Get Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.x

### Setting Up Keycloak Version 8

1. **[Install docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/)**

2. **Start Keycloak using Docker Compose**

   ```bash
   docker-compose up -d
   ```

   This command will start a Keycloak instance with version 8 and Postgres 11. Postgres data will be stored in the `postgres_data` docker volume.

## Scripts

### Keycloak User Generation Script

This specific script generates 50,000 Keycloak users in the `test` realm using the Keycloak API. The script creates users with some random attributes to avoid duplicates.

### Prerequisites

- Python 3.x
- Keycloak server running and accessible
- Keycloak admin credentials

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-repository-name.git
   cd your-repository-name
   ```

2. **Create and activate a virtual environment**

   - On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Update the `create_keycloak_users.py` script with your Keycloak server configuration:

```python
# Keycloak server configuration
KEYCLOAK_URL = "http://localhost:8080"
REALM = "test"
CLIENT_ID = "admin-cli"
USERNAME = "admin"
PASSWORD = "admin"
```

### Usage

Run the script to start generating users:

```bash
python create_keycloak_users.py
```

The script will authenticate with Keycloak, generate user data, and create 50,000 users in the specified realm. Progress will be printed every 100 users.

### Notes

- Ensure your Keycloak server is running and accessible at the URL specified in the script.
- Make sure the admin user credentials are correct and have the necessary permissions to create users.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
