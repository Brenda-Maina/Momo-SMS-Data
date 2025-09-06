# High-Level System Architecture — Momo-SMS Data Pipeline

**One-sentence summary:**  
This ETL pipeline ingests mobile-money SMS XML, parses and maps the schema, normalizes and classifies transactions, persists them to a relational store, and exposes analytics for visualization.

## Main Components (top → bottom)
1. **Mobile Money XML Ingestion Layer (SMS INPUT)**  
   Entry point for raw MoMo XML messages.

2. **XML Parsing & Data Extraction**  
   Extracts transaction fields and maps XML nodes to internal schema.

3. **Data Normalization & Transaction Classification**  
   Standardizes amounts/dates/phones and assigns transaction category labels.

4. **SQLite Database**  
   Persistent storage with a `transactions` table (relational model).

5. **Analytics & Visualization Layer**  
   Dashboard and reporting layer that consumes aggregated JSON or API endpoints.

6. **Pipeline Termination Node**  
   Marks the end of the processing flow/lifecycle.

## Minimal DB idea
Proposed table:  
`transactions(id, momo_id, sender, receiver, amount_cents, currency, transaction_date, narration, category, raw_text)`

> Notes: store money as integer cents. Keep `data/raw/` and `data/db.sqlite3` git-ignored.

![Architecture Diagram](architecture_diagram.png)
