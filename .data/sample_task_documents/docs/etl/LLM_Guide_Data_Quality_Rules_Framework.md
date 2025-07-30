# Data Cleaning Rules and Strategies Framework

## Overview

This document outlines a comprehensive approach to data cleansing for tables in a data warehouse environment. It provides a structured methodology for identifying data quality issues and implementing appropriate cleaning solutions.

## Process Framework

### Step 1: Schema Analysis

#### 1.1 Schema Retrieval and Documentation
```sql
-- Retrieve table schema information
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable, 
    column_default
FROM 
    information_schema.columns
WHERE 
    table_name = '[TABLE_NAME]'
    AND table_schema = '[SCHEMA_NAME]';

-- Retrieve primary key information
SELECT 
    tc.constraint_name, 
    kcu.column_name
FROM 
    information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
WHERE 
    tc.constraint_type = 'PRIMARY KEY' 
    AND tc.table_name = '[TABLE_NAME]'
    AND tc.table_schema = '[SCHEMA_NAME]';

-- Retrieve foreign key information
SELECT 
    tc.constraint_name, 
    kcu.column_name,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column
FROM 
    information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu
        ON tc.constraint_name = ccu.constraint_name
WHERE 
    tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name = '[TABLE_NAME]'
    AND tc.table_schema = '[SCHEMA_NAME]';
```

#### 1.2 Schema Analysis Checklist
- [ ] Identify primary and foreign keys
- [ ] Note nullable vs. non-nullable columns
- [ ] Document data types and length constraints
- [ ] Identify columns with default values
- [ ] Document unique constraints and indexes
- [ ] Identify columns requiring special attention based on data type or business importance

### Step 2: Data Profiling

#### 2.1 Basic Statistics
```sql
-- Row count
SELECT COUNT(*) FROM [TABLE_NAME];

-- Null count and percentage for each column
SELECT
    COUNT(*) AS total_rows,
    [COLUMN_LIST_WITH_NULL_COUNTS_AND_PERCENTAGES]
FROM
    [TABLE_NAME];
```

#### 2.2 Duplicate Analysis
```sql
-- Identify duplicates across key fields
SELECT 
    [KEY_COLUMNS], 
    COUNT(*) as duplicate_count
FROM 
    [TABLE_NAME]
GROUP BY 
    [KEY_COLUMNS]
HAVING 
    COUNT(*) > 1;
```

#### 2.3 Text Column Analysis
```sql
-- For categorical columns: distinct value counts
SELECT 
    [COLUMN_NAME], 
    COUNT(*) as frequency
FROM 
    [TABLE_NAME]
GROUP BY 
    [COLUMN_NAME]
ORDER BY 
    frequency DESC;

-- Check for inconsistent formatting, trailing spaces
SELECT 
    [COLUMN_NAME],
    LENGTH([COLUMN_NAME]) as field_length,
    COUNT(*) as count
FROM 
    [TABLE_NAME]
WHERE 
    [COLUMN_NAME] IS NOT NULL
GROUP BY 
    [COLUMN_NAME], field_length
ORDER BY 
    field_length DESC;

-- Check for mixed case issues
SELECT 
    CASE 
        WHEN [COLUMN_NAME] = UPPER([COLUMN_NAME]) THEN 'UPPER'
        WHEN [COLUMN_NAME] = LOWER([COLUMN_NAME]) THEN 'lower'
        WHEN [COLUMN_NAME] = INITCAP([COLUMN_NAME]) THEN 'Title Case'
        ELSE 'Mixed Case'
    END as case_type,
    COUNT(*) as count
FROM 
    [TABLE_NAME]
WHERE 
    [COLUMN_NAME] IS NOT NULL
GROUP BY 
    case_type;

-- Pattern analysis for ID fields or formatted values
SELECT 
    REGEXP_REPLACE([COLUMN_NAME], '[0-9]', '#') as pattern,
    COUNT(*) as count
FROM 
    [TABLE_NAME]
WHERE 
    [COLUMN_NAME] IS NOT NULL
GROUP BY 
    pattern
ORDER BY 
    count DESC;
```

#### 2.4 Numeric Column Analysis
```sql
-- Basic statistics for numeric columns
SELECT
    MIN([COLUMN_NAME]) as minimum,
    MAX([COLUMN_NAME]) as maximum,
    AVG([COLUMN_NAME]) as average,
    STDDEV([COLUMN_NAME]) as standard_deviation,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY [COLUMN_NAME]) as median
FROM
    [TABLE_NAME]
WHERE
    [COLUMN_NAME] IS NOT NULL;

-- Outlier identification (values outside 3 standard deviations)
WITH stats AS (
    SELECT
        AVG([COLUMN_NAME]) as avg_value,
        STDDEV([COLUMN_NAME]) as stddev_value
    FROM
        [TABLE_NAME]
    WHERE
        [COLUMN_NAME] IS NOT NULL
)
SELECT
    [COLUMN_NAME],
    ([COLUMN_NAME] - avg_value) / stddev_value as z_score
FROM
    [TABLE_NAME], stats
WHERE
    [COLUMN_NAME] IS NOT NULL
    AND ABS(([COLUMN_NAME] - avg_value) / stddev_value) > 3
ORDER BY
    ABS(([COLUMN_NAME] - avg_value) / stddev_value) DESC;

-- Value distribution by range buckets
SELECT
    NTILE(10) OVER (ORDER BY [COLUMN_NAME]) as bucket,
    MIN([COLUMN_NAME]) as min_value,
    MAX([COLUMN_NAME]) as max_value,
    COUNT(*) as count
FROM
    [TABLE_NAME]
WHERE
    [COLUMN_NAME] IS NOT NULL
GROUP BY
    bucket
ORDER BY
    bucket;
```

#### 2.5 Date Column Analysis
```sql
-- Date range analysis
SELECT
    MIN([DATE_COLUMN]) as earliest_date,
    MAX([DATE_COLUMN]) as latest_date,
    MAX([DATE_COLUMN]) - MIN([DATE_COLUMN]) as date_range_days
FROM
    [TABLE_NAME]
WHERE
    [DATE_COLUMN] IS NOT NULL;

-- Check for dates outside business timeframe
SELECT
    COUNT(*) as count,
    'Future dates' as issue
FROM
    [TABLE_NAME]
WHERE
    [DATE_COLUMN] > CURRENT_DATE
UNION ALL
SELECT
    COUNT(*) as count,
    'Before business start' as issue
FROM
    [TABLE_NAME]
WHERE
    [DATE_COLUMN] < '[BUSINESS_START_DATE]';

-- Date integrity between related columns
SELECT
    COUNT(*) as invalid_count
FROM
    [TABLE_NAME]
WHERE
    [END_DATE] < [START_DATE];

-- Distribution by time periods
SELECT
    EXTRACT(YEAR FROM [DATE_COLUMN]) as year,
    EXTRACT(MONTH FROM [DATE_COLUMN]) as month,
    COUNT(*) as record_count
FROM
    [TABLE_NAME]
WHERE
    [DATE_COLUMN] IS NOT NULL
GROUP BY
    year, month
ORDER BY
    year, month;
```

#### 2.6 Relationship Integrity Analysis
```sql
-- Check for orphaned records (foreign key violations)
SELECT
    COUNT(*) as orphaned_records
FROM
    [TABLE_NAME] t
    LEFT JOIN [REFERENCED_TABLE] r
        ON t.[FOREIGN_KEY] = r.[REFERENCED_KEY]
WHERE
    t.[FOREIGN_KEY] IS NOT NULL
    AND r.[REFERENCED_KEY] IS NULL;
```

### Step 3: Cleaning Rules Development

Based on the data profiling results, develop specific cleaning rules for each type of data quality issue identified:

#### 3.1 Missing Values Strategy

| Column | Missing Value Strategy | Justification |
|--------|------------------------|---------------|
| Column1 | Reject (enforce NOT NULL) | Critical business data that must be provided |
| Column2 | Default value (specify) | Optional field with logical default |
| Column3 | Imputation strategy (specify) | Derivable from other fields |

#### 3.2 Text Standardization Rules

| Column | Standardization Rule | Example |
|--------|---------------------|---------|
| Name | Title case, trim spaces | "john doe" → "John Doe" |
| AddressLine | Upper case, trim spaces | "123 main st. " → "123 MAIN ST." |
| Code | Format pattern XXX-YYY-ZZZ | "ABC123456" → "ABC-123-456" |

#### 3.3 Numeric Validation Rules

| Column | Validation Rule | Outlier Handling |
|--------|----------------|------------------|
| Age | Between 0-120 | Cap at max/min |
| Price | Positive, max 4 decimal places | Flag for review if >3σ from mean |
| Quantity | Integer, minimum 1 | Reject if outside valid range |

#### 3.4 Date Consistency Rules

| Column | Consistency Rule | Invalid Date Handling |
|--------|-----------------|----------------------|
| BirthDate | Not in future, not before 1900 | Reject if outside range |
| StartDate/EndDate | EndDate ≥ StartDate | Flag for review |
| TransactionDate | Within business timeframe | Reject if outside window |

#### 3.5 Duplicate Handling Strategy

| Entity | Duplicate Definition | Resolution Strategy |
|--------|---------------------|---------------------|
| Customer | Same Email + Phone | Keep newest record |
| Transaction | Same Reference Number | Flag as potential duplicate for review |
| Product | Same SKU | Consolidate and update metadata |

#### 3.6 Referential Integrity Enforcement

| Foreign Key | Constraint | Orphaned Record Handling |
|-------------|-----------|--------------------------|
| CustomerId | Must exist in Customers | Flag for review |
| ProductId | Must exist in Products | Reject |

### Step 4: Implementation Plan

#### 4.1 SQL Implementation Template
```sql
-- Template for cleaning implementation script
-- [RULE_DESCRIPTION]
BEGIN TRANSACTION;

-- Log cleaning operation start
INSERT INTO data_cleaning_log (
    table_name, rule_name, start_time, affected_rows_expected
)
VALUES (
    '[TABLE_NAME]', 
    '[RULE_NAME]', 
    CURRENT_TIMESTAMP,
    (SELECT COUNT(*) FROM [TABLE_NAME] WHERE [CONDITION])
);

-- Create backup of affected rows
SELECT * INTO [BACKUP_TABLE]
FROM [TABLE_NAME]
WHERE [CONDITION];

-- Perform cleaning operation
UPDATE [TABLE_NAME]
SET
    [COLUMN_NAME] = [NEW_VALUE]
WHERE
    [CONDITION];

-- Log cleaning operation completion
UPDATE data_cleaning_log
SET
    end_time = CURRENT_TIMESTAMP,
    affected_rows_actual = @@ROWCOUNT,
    status = 'COMPLETED'
WHERE
    table_name = '[TABLE_NAME]'
    AND rule_name = '[RULE_NAME]'
    AND end_time IS NULL;

COMMIT;
```

#### 4.2 Cleaning Script Sequence

Implement cleaning operations in the following order to ensure dependencies are handled:

1. **Missing Values Resolution**
   - Handle nullable columns first
   - Apply default values
   - Implement imputation strategies

2. **Format Standardization**
   - Standardize case formatting
   - Remove extra spaces and special characters
   - Apply pattern formatting

3. **Validation Rules**
   - Apply range constraints for numeric values
   - Apply date validation and consistency checks
   - Apply pattern validation for formatted fields

4. **Duplication Resolution**
   - Identify and handle duplicate records
   - Merge or remove duplicates according to strategy

5. **Referential Integrity**
   - Handle orphaned records
   - Enforce foreign key constraints

#### 4.3 Cleaning Impact Measurement

After each cleaning operation, measure and document the impact using metrics such as:

- Number of records affected
- Percentage of data cleaned
- Before/after statistics for key quality indicators
- Performance metrics (execution time, resource usage)

## Conclusion and Next Steps

After completing the data cleansing process:

1. Document all applied cleaning rules and their impact
2. Implement ongoing data quality monitoring
3. Create data quality dashboards for continuous tracking
4. Establish data governance procedures to prevent future quality issues
5. Develop a maintenance plan for periodic cleaning operations

---

## Implementation Template for [TABLE_NAME]

### Step 1: Schema Analysis Results

*(To be completed after analyzing actual schema)*

### Step 2: Data Profiling Results

*(To be completed after profiling actual data)*

### Step 3: Cleaning Rules for [TABLE_NAME]

*(To be completed based on profiling results)*

### Step 4: Implementation Scripts

*(To be completed with actual cleaning scripts)*
