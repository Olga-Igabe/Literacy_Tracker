from mysql.connector import Error

def register_member(conn):
    print("\n--- Register New Member ---")
    name = input("Enter member's full name: ").strip()
    contact = input("Enter contact details: ").strip()
    
    while True:
        age_group = input("Enter age group (Child/Youth/Adult): ").strip().capitalize()
        if age_group in ["Child", "Youth", "Adult"]:
            break
        print("❌ Invalid input. Please enter exactly Child, Youth, or Adult.")
        
    guardian_name = None
    guardian_contact = None
    
    if age_group in ["Child", "Youth"]:
        is_under_18 = input("Is the member under 18? (yes/no): ").strip().lower()
        if is_under_18 in ['yes', 'y']:
            guardian_name = input("Enter guardian's name: ").strip()
            guardian_contact = input("Enter guardian's contact details: ").strip()

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO members (name, contact, age_group, guardian_name, guardian_contact)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, contact, age_group, guardian_name, guardian_contact))
        conn.commit()
        print(f"✅ Successfully registered {name}!")
        
    except Error as e:
        print(f"❌ Database error while registering member: {e}")
        conn.rollback()
    finally:
        cursor.close()


def update_progress(conn):
    print("\n--- Update Member Progress ---")
    search_name = input("Enter the member's name to look up: ").strip()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT member_id, name FROM members WHERE name LIKE %s", (f"%{search_name}%",))
        results = cursor.fetchall()
        
        if not results:
            print("❌ No member found with that name.")
            return
        
        if len(results) > 1:
            print("\nMultiple members found. Please select the correct one:")
            for idx, row in enumerate(results):
                print(f"[{idx + 1}] Member ID: {row[0]} | Name: {row[1]}")
            
            while True:
                try:
                    choice = int(input("Enter the list number of the correct member: ")) - 1
                    if 0 <= choice < len(results):
                        member_id = results[choice][0]
                        member_name = results[choice][1]
                        break
                    print("❌ Choice out of range.")
                except ValueError:
                    print("❌ Please enter a valid number.")
        else:
            member_id = results[0][0]
            member_name = results[0][1]
            
        skill_name = input("Enter skill name (e.g., Phonics, Reading Comprehension): ").strip()
        
        while True:
            status_input = input("Enter status (Not Started/In Progress/Completed): ").strip()
            status = " ".join([word.capitalize() for word in status_input.split()])
            if status in ["Not Started", "In Progress", "Completed"]:
                break
            print("❌ Invalid status. Please choose: Not Started, In Progress, or Completed.")
            
        sql = """
            INSERT INTO member_progress (member_id, skill_name, status)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """
        cursor.execute(sql, (member_id, skill_name, status))
        conn.commit()
        print(f"✅ Successfully updated progress for {member_name} on '{skill_name}' to '{status}'.")
        
    except Error as e:
        print(f"❌ Database error while updating progress: {e}")
        conn.rollback()
    finally:
        cursor.close()