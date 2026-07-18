#!/usr/bin/env python3
"""Main menu for the Community Literacy & Device Tracker project."""

from database import get_connection
from members import register_member, update_progress
from devices import add_device, lend_device, return_device
from workshops import log_workshop
from reports import members_by_age_group, devices_on_loan, overdue_devices


def print_menu():
    print("\n=== Community Tracker Menu ===")
    print("1. Register new member")
    print("2. Update member skill progress")
    print("3. Add new device")
    print("4. Lend device")
    print("5. Return device")
    print("6. Log workshop attendance")
    print("7. View reports")
    print("0. Exit")


def reports_menu(conn):
    print("\n--- Reports ---")
    print("a. Members trained by age group")
    print("b. Devices currently on loan")
    print("c. Overdue devices")
    choice = input("Choose a report (a/b/c): ").strip().lower()
    if choice == "a":
        members_by_age_group(conn)
    elif choice == "b":
        devices_on_loan(conn)
    elif choice == "c":
        overdue_devices(conn)
    else:
        print("Invalid report choice.")


def main():
    conn = get_connection()
    try:
        while True:
            print_menu()
            choice = input("Choose an option (0-7): ").strip()

            if choice == "1":
                register_member(conn)
            elif choice == "2":
                update_progress(conn)
            elif choice == "3":
                add_device(conn)
            elif choice == "4":
                lend_device(conn)
            elif choice == "5":
                return_device(conn)
            elif choice == "6":
                log_workshop(conn)
            elif choice == "7":
                reports_menu(conn)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 0 to 7.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
