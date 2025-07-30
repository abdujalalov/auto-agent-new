# PostgreSQL Command Line Access Guide

This document provides comprehensive guidance for accessing and working with PostgreSQL databases through command line tools, with special attention to character encoding and internationalization.

## Connection Information

Use the following connection details to access the database:

```
Host:           127.0.0.1  
Port:           5432  
User:           postgres  
Password:       web@1234  
Database:       Superstore  
```

### Connection String Formats

#### Standard Connection URI:

```
postgresql://postgres:web@1234@127.0.0.1:5432/Superstore
```

#### Libpq Format (used in tools like `psql`):

```
host=127.0.0.1 port=5432 dbname=Superstore user=postgres password=web@1234
```

> **Security Note**: This connection information should be used only for development and testing environments. In production, use appropriate security measures and avoid hardcoding credentials.

## Command Line Tools

### `psql` Utility

Connect to the database:

```bash
PGPASSWORD=web@1234 psql -h 127.0.0.1 -U postgres -d Superstore
```

Run queries:

```sql
SELECT * FROM Orders;
```

Exit:

```
\q
```

#### `psql` with Encoding Support

When working with non-ASCII characters (e.g., Cyrillic), ensure the client encoding is set:

```bash
PGPASSWORD=web@1234 psql -h 127.0.0.1 -U postgres -d Superstore -c "SET client_encoding TO 'WIN1251'; SELECT * FROM Orders;"
```

Key parameters:

* `-h`: Host
* `-U`: Username
* `-d`: Database name
* `-c`: SQL command
* `PGPASSWORD`: Password environment variable (avoid interactive prompt)

### PowerShell

Basic connection and query using `Npgsql` (.NET PostgreSQL driver):

```powershell
Add-Type -Path "Npgsql.dll"
$connString = "Host=127.0.0.1;Port=5432;Username=postgres;Password=web@1234;Database=Superstore"
$conn = New-Object Npgsql.NpgsqlConnection($connString)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM Orders"
$reader = $cmd.ExecuteReader()

while ($reader.Read()) {
    $reader[0]  # Process results
}

$reader.Close()
$conn.Close()
```

#### PowerShell with JSON Output (for LLMs)

```powershell
$connString = "Host=127.0.0.1;Port=5432;Username=postgres;Password=web@1234;Database=Superstore"
$conn = New-Object Npgsql.NpgsqlConnection($connString)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM Orders"
$reader = $cmd.ExecuteReader()

$results = @()
while ($reader.Read()) {
    $row = @{}
    for ($i = 0; $i -lt $reader.FieldCount; $i++) {
        $row[$reader.GetName($i)] = $reader[$i]
    }
    $results += $row
}

$reader.Close()
$conn.Close()

$results | ConvertTo-Json -Depth 10
```

### Data Import/Export

#### Export using `COPY`:

```bash
PGPASSWORD=web@1234 psql -h 127.0.0.1 -U postgres -d Superstore -c "\COPY Orders TO 'output.csv' CSV HEADER"
```

#### Import using `COPY`:

```bash
PGPASSWORD=web@1234 psql -h 127.0.0.1 -U postgres -d Superstore -c "\COPY Orders FROM 'input.csv' CSV HEADER"
```

### Alternative: Use `pg_dump` and `psql` for full backups and restores.

## Character Encoding Considerations

### Supported Encodings

| Encoding | Description                  |
| -------- | ---------------------------- |
| UTF8     | Recommended for multilingual |
| WIN1251  | Windows Cyrillic (legacy)    |
| LATIN1   | Western European (legacy)    |

### Setting Encoding

Ensure the database is created with correct encoding, or use client-side override:

```bash
psql -h 127.0.0.1 -U postgres -d Superstore -c "SET client_encoding = 'WIN1251';"
```

### Working with Non-ASCII Data

1. Use proper encoding at both DB and client sides.
2. Validate file encodings when importing/exporting.
3. Use `\encoding` in `psql` to check or set encoding.

## Troubleshooting

| Issue                             | Solution                                |
| --------------------------------- | --------------------------------------- |
| Garbled Cyrillic output           | Use `SET client_encoding TO 'WIN1251'`  |
| Password prompt stalls in scripts | Use `PGPASSWORD` environment variable   |
| Unicode characters not displaying | Use `UTF8` and proper terminal settings |
| CSV import fails                  | Check encoding and column mismatch      |

## Script Execution Process

```bash
# 1. Save SQL to file
echo "SELECT * FROM Orders;" > query.sql

# 2. Execute the SQL file
PGPASSWORD=web@1234 psql -h 127.0.0.1 -U postgres -d Superstore -f query.sql
```

---

This document serves as a reference for working with PostgreSQL databases through command line tools, with special focus on proper encoding and internationalization support.
