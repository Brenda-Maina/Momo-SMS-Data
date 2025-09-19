# MOMO SMS Data Project

## Team Information
**Team Name:** Team 1

**Members:**
- Angel Kibui
- Brenda Maina
- Ndunge Mbithi

---

## Project Description
This project builds an enterprise-style fullstack application to process and analyze MoMo SMS transaction data. The system ingests raw MoMo SMS XML files, extracts transaction fields, cleans and normalizes timestamps, phone numbers and amounts, and categorizes transactions (e.g., inflow, outflow). Processed records are stored in a SQLite database and aggregated into a `dashboard.json` file used by a lightweight HTML/JS dashboard to display charts and transaction tables.

The project emphasizes a reproducible ETL pipeline, clean data handling, collaborative development (Codespaces, branching, PRs), and an architecture that supports adding a REST API (FastAPI) for integrations.

---

## Scrum Board
We manage project tasks using a task board (ClickUp/Trello).  
[View our Scrum Board here](https://app.clickup.com/90121191829/v/li/901212276633)

# Momo-SMS-Data
Enterprise fullstack app to process MoMo SMS XML, store in SQLite, and visualize analytics.
## 🏗️ System Architecture

This repository implements a simple ETL pipeline for mobile money SMS data.  
See the high-level flow and diagram below.

![System Architecture](docs/architecture_diagram.png)

## Database Design

Our MoMo SMS Data Processing System is supported by a MySQL database designed to ensure data integrity, scalability, and efficient querying. The schema was derived from the XML transaction structure and the ERD.

### Schema Overview
- **Users**: Stores sender and receiver information.  
- **Transactions**: Core table containing transaction records such as amount, timestamp, and status.  
- **Transaction_Categories**: Defines types of transactions including deposits, withdrawals, and payments.  
- **System_Logs**: Tracks data processing activities for auditing and debugging purposes.  
- **Channels**: Represents the communication medium, for example SMS or USSD.  
- **Assignments**: Maps transactions to categories or channels, resolving many-to-many relationships.  

### Constraints and Integrity
- Each table uses primary keys (PK) for unique identification.  
- Foreign keys (FK) enforce relationships between entities.  
- CHECK constraints validate data integrity, for example ensuring that transaction amounts are greater than zero.  
- Indexes were added on frequently queried fields such as `transaction_date` and `user_id` to improve performance.  

### Sample Data
The database includes five test records per main table for validation. CRUD operations (Create, Read, Update, Delete) were successfully tested to confirm functionality.  

### Design Rationale
- **Normalization**: Data is stored in a normalized structure to reduce redundancy.  
- **Scalability**: Tables such as `Transaction_Categories` and `Channels` make the schema extensible.  
- **Traceability**: `System_Logs` ensure transparent tracking of processing steps.  

The SQL setup script can be found here:  
[`database/database_setup.sql`](./database/database_setup.sql)

## JSON Data Models

JSON schemas have been created in examples/json_schemas.json that:

- Match the MySQL database structure exactly
- Include examples for all 6 database tables
- Show complete transaction objects with nested relationships
- Demonstrate API response formats
- Document the SQL-to-JSON field mapping

See examples/JSON_MAPPING_GUIDE.md for complete documentation. 
