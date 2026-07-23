"""Generates summary reports from the literacy tracker database."""


def members_by_age_group(conn):
    """Report: count of members trained (completed at least one skill),
    grouped by age group.

    Args:
        conn: an active MySQL connection.
    """
    cursor = conn.cursor()
    query = """
        SELECT m.age_group, COUNT(DISTINCT m.member_id) AS trained_count
        FROM members m
        JOIN member_progress mp ON m.member_id = mp.member_id
        WHERE mp.status = 'Completed'
        GROUP BY m.age_group
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    print("\nMembers Trained by Age Group:")
    if not results:
        print("  No completed training records yet.")
        return

    for age_group, count in results:
        print(f"  {age_group}: {count}")


def devices_on_loan(conn):
    """Report: list of devices currently on loan, with borrower and due
    date.

    Args:
        conn: an active MySQL connection.
    """
    cursor = conn.cursor()
    query = """
        SELECT d.device_name, m.full_name, l.due_date
        FROM loans l
        JOIN devices d ON l.device_id = d.device_id
        JOIN members m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    print("\nDevices Currently On Loan:")
    if not results:
        print("  No devices currently on loan.")
        return

    for device_name, borrower, due_date in results:
        print(f"  {device_name} -> {borrower} (due {due_date})")


def overdue_devices(conn):
    """Report: devices past their due date that haven't been returned.

    Args:
        conn: an active MySQL connection.
    """
    cursor = conn.cursor()
    query = """
        SELECT d.device_name, m.full_name, l.due_date
        FROM loans l
        JOIN devices d ON l.device_id = d.device_id
        JOIN members m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL AND l.due_date < CURDATE()
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    print("\nOverdue Devices:")
    if not results:
        print("  No overdue devices.")
        return

    for device_name, borrower, due_date in results:
        print(f"  {device_name} -> {borrower} (was due {due_date})")


def view_reports(conn):
    """Menu entry point: run all three reports in sequence.

    Args:
        conn: an active MySQL connection.
    """
    members_by_age_group(conn)
    devices_on_loan(conn)
    overdue_devices(conn)