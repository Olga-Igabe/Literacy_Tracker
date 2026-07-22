from mysql.connector import Error


def log_workshop(conn):
    """
    Logs a new workshop, then records attendance for one or more members.
    Matches the single-argument call signature main.py expects:
        log_workshop(conn)
    """
    print("\n--- Log Workshop & Attendance ---")
    workshop_name = input("Enter workshop name: ").strip()
    topic = input("Enter workshop topic: ").strip()
    workshop_date = input("Enter workshop date (YYYY-MM-DD): ").strip()

    try:
        cursor = conn.cursor()

        # 1. Insert the workshop record
        cursor.execute(
            """
            INSERT INTO workshops (workshop_name, workshop_date, topic)
            VALUES (%s, %s, %s)
            """,
            (workshop_name, workshop_date, topic),
        )
        conn.commit()
        workshop_id = cursor.lastrowid
        print(f"✅ Workshop '{workshop_name}' logged with ID {workshop_id}.")

        # 2. Record attendance for one or more members
        while True:
            search_name = input(
                "\nEnter attendee's name to search (or leave blank to finish): "
            ).strip()
            if not search_name:
                break

            cursor.execute(
                "SELECT member_id, name FROM members WHERE name LIKE %s",
                (f"%{search_name}%",),
            )
            results = cursor.fetchall()

            if not results:
                print("❌ No member found with that name.")
                continue

            if len(results) > 1:
                print("\nMultiple members found. Please select the correct one:")
                for idx, row in enumerate(results):
                    print(f"[{idx + 1}] Member ID: {row[0]} | Name: {row[1]}")

                member_id = None
                while member_id is None:
                    try:
                        choice = int(input("Enter the list number of the correct member: ")) - 1
                        if 0 <= choice < len(results):
                            member_id = results[choice][0]
                            member_name = results[choice][1]
                        else:
                            print("❌ Choice out of range.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
            else:
                member_id = results[0][0]
                member_name = results[0][1]

            # Prevent duplicate attendance entries for the same workshop
            cursor.execute(
                "SELECT 1 FROM workshop_attendance WHERE workshop_id = %s AND member_id = %s",
                (workshop_id, member_id),
            )
            if cursor.fetchone():
                print(f"❌ {member_name} is already marked as attending this workshop.")
                continue

            cursor.execute(
                """
                INSERT INTO workshop_attendance (workshop_id, member_id)
                VALUES (%s, %s)
                """,
                (workshop_id, member_id),
            )
            conn.commit()
            print(f"✅ Attendance recorded for {member_name}.")

    except Error as e:
        print(f"❌ Database error while logging workshop: {e}")
        conn.rollback()
    finally:
        cursor.close()