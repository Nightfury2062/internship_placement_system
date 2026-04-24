import mysql.connector

# -----------------------------
# Database Connection
# -----------------------------
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="rohit123",
    database="internship_placement_db"
)
cursor = db.cursor()

# -----------------------------
# View Jobs
# -----------------------------
def view_jobs():
    query = """
    SELECT Job_Posting.job_id,
           Job_Posting.role,
           Company.company_name,
           Job_Posting.salary
    FROM Job_Posting
    JOIN Company
    ON Job_Posting.company_id = Company.company_id
    WHERE Job_Posting.status = 'approved'
    ORDER BY Job_Posting.salary DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print("\nAvailable Jobs:")
    print(f"{'ID':<6} {'Role':<35} {'Company':<20} {'Salary (Rs.)'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<35} {row[2]:<20} {row[3]:,.0f}")

# -----------------------------
# Apply Job (inserts into Offer)
# -----------------------------
def apply_job(student_id, job_id):
    cursor.execute(
        "SELECT offer_id FROM Offer WHERE student_id = %s AND job_id = %s",
        (student_id, job_id)
    )
    if cursor.fetchone():
        print("⚠️  You have already applied for this job.")
        return

    try:
        cursor.execute(
            "INSERT INTO Offer (student_id, job_id, offer_status) VALUES (%s, %s, 'pending')",
            (student_id, job_id)
        )
        db.commit()
        print("✅ Application submitted successfully.")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)

# -----------------------------
# View Applications
# -----------------------------
def view_applications(student_id):
    query = """
    SELECT
        Offer.offer_id,
        Job_Posting.role,
        Company.company_name,
        Offer.offer_status
    FROM Offer
    JOIN Job_Posting ON Offer.job_id = Job_Posting.job_id
    JOIN Company     ON Job_Posting.company_id = Company.company_id
    WHERE Offer.student_id = %s
    ORDER BY Offer.offer_id DESC
    """
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    if not rows:
        print("\nNo applications found for this student.")
        return
    print("\nYour Applications:")
    print(f"{'Offer ID':<10} {'Role':<35} {'Company':<20} {'Status'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<10} {row[1]:<35} {row[2]:<20} {row[3]}")

# -----------------------------
# Add Student
# -----------------------------
def add_student():
    print("\n--- Add New Student ---")
    roll   = input("Roll Number : ").strip()
    name   = input("Name        : ").strip()
    branch = input("Branch      : ").strip()
    batch  = input("Batch Year  : ").strip()
    cgpa   = input("CGPA        : ").strip()

    if not all([roll, name, branch, batch, cgpa]):
        print("❌ All fields are required.")
        return

    try:
        email = roll + "@mail.com"
        cursor.execute(
            """
            INSERT INTO Student (roll_number, name, branch, batch, cgpa, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (roll, name, branch, int(batch), float(cgpa), email)
        )
        db.commit()
        new_id = cursor.lastrowid
        print(f"✅ Student '{name}' added successfully!")
        print(f"   📋 Student ID : {new_id}")
        print(f"   📧 Email      : {email}")
        print(f"   👉 Use Student ID {new_id} to apply for jobs.")

    except ValueError:
        print("❌ Batch must be a whole number and CGPA must be a decimal.")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)

# -----------------------------
# View All Students
# -----------------------------
def view_students():
    cursor.execute("""
        SELECT student_id, roll_number, name, branch, batch, cgpa
        FROM Student
        ORDER BY student_id
    """)
    rows = cursor.fetchall()
    print("\nAll Students:")
    print(f"{'ID':<6} {'Roll':<12} {'Name':<20} {'Branch':<18} {'Batch':<8} {'CGPA'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<12} {row[2]:<20} {row[3]:<18} {row[4]:<8} {row[5]}")

# -----------------------------
# Main Menu
# -----------------------------
while True:
    print("\n========== Placement Portal ==========")
    print("1. View Jobs")
    print("2. Apply for a Job")
    print("3. My Applications")
    print("4. Add Student")
    print("5. View All Students")
    print("6. Exit")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        view_jobs()
    elif choice == "2":
        try:
            s = int(input("Student ID: "))
            j = int(input("Job ID: "))
            apply_job(s, j)
        except ValueError:
            print("❌ Please enter valid numeric IDs.")
    elif choice == "3":
        try:
            s = int(input("Student ID: "))
            view_applications(s)
        except ValueError:
            print("❌ Please enter a valid numeric ID.")
    elif choice == "4":
        add_student()
    elif choice == "5":
        view_students()
    elif choice == "6":
        print("Goodbye!")
        cursor.close()
        db.close()
        break
    else:
        print("Invalid choice. Please enter 1-6.")