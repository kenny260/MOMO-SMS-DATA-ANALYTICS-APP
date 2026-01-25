# Database Design Rationale

## Entity Selection

The database design identifies four core entities from the MoMo SMS transaction data:

**Transactions** stores all mobile money transaction records including amount, type, timestamp, and status. This central entity represents the primary business operation.

**Users** captures customer information for both senders and receivers. Separating user data from transactions eliminates redundancy and enables efficient customer management across multiple transactions.

**Transaction_Categories** normalizes transaction types (SEND, RECEIVE, DEPOSIT, WITHDRAW, PAYMENT) into a dedicated table. This supports easy category additions, consistent categorization, and simplified reporting.

**System_Logs** tracks all data processing activities, errors, and system events. This audit trail is essential for debugging, monitoring system health, and maintaining data integrity throughout the ETL pipeline.

## Relationship Design

The design implements several key relationships:

**Users to Transactions (1:M)**: One user can participate in many transactions as either sender or receiver, requiring two foreign keys in Transactions (sender_id, receiver_id).

**Transaction_Categories to Transactions (1:M)**: Each category classifies many transactions, while each transaction belongs to exactly one category.

**Users to System_Logs (M:N)**: Multiple users can be involved in multiple log entries, and vice versa. This many-to-many relationship is resolved using User_Logs junction table, enabling tracking of which users were affected by specific system events.

## Constraints and Integrity

Primary keys ensure unique record identification. Foreign keys maintain referential integrity, preventing orphaned records. CHECK constraints validate data ranges (amount > 0, sender ≠ receiver). Indexes on frequently queried fields (transaction dates, phone numbers) optimize query performance. Security triggers log all transaction inserts and prevent deletion of completed transactions, ensuring data integrity and audit compliance.
