# JSON Mapping Guide - Database to JSON

## Database Schema to JSON Structure

### Table: users → user_example
- Direct field mapping with same names
- All fields included in JSON

### Table: transactions → transaction_example  
- amount_cents converted to amount_decimal (cents / 100)
- balance_cents converted to balance_decimal
- currency renamed to amount_currency for clarity

### Table: assignments → assignment_example
- Direct mapping with foreign keys
- Used in complete transaction responses

### Complete Transaction Structure
The `complete_transaction_example` demonstrates:
- Transaction details with computed decimal amounts
- Nested sender/receiver user objects
- Channel information
- Multiple categories (many-to-many via assignments)
- Processing logs
- Assignment history

## API Response Formats

### Single Transaction
```json
{
  "success": true,
  "data": {complete_transaction_object},
  "metadata": {...}
}
