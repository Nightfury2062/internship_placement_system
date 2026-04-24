import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import platform

# -----------------------------
# Database Connection
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rohit123",
    database="internship_placement_db",
    # unix_socket="/tmp/mysql.sock" # Uncomment if your Mac needs this for MySQL
)
cursor = db.cursor()

# -----------------------------
# Color Palette — Light Theme
# -----------------------------
BG        = "#F4F7FE"  
PANEL     = "#FFFFFF"  
BORDER    = "#E2E8F0"  
PRIMARY   = "#4318FF"  
SECONDARY = "#FF7043"  
SUCCESS   = "#05CD99"  
TEXT      = "#2B3674"  
SUBTEXT   = "#A3AED0"  
ENTRY_BG  = "#FFFFFF"  
HEADER_BG = "#F4F7FE"  

# -----------------------------
# Animated Hover Button
# -----------------------------
class AnimButton(tk.Label):
    def __init__(self, parent, text, command=None, color=PRIMARY, width=14, **kwargs):
        super().__init__(
            parent, text=text, bg=color, fg="white",
            font=("Helvetica", 10, "bold"),
            cursor="hand2", width=width, pady=10, **kwargs
        )
        self._color = color
        self._cmd   = command
        self._dark  = self._darken(color)
        self.bind("<Enter>",   lambda e: self.config(bg=self._dark))
        self.bind("<Leave>",   lambda e: self.config(bg=self._color))
        self.bind("<Button-1>", lambda e: self._cmd() if self._cmd else None)

    @staticmethod
    def _darken(hex_color):
        r = max(0, int(hex_color[1:3], 16) - 20)
        g = max(0, int(hex_color[3:5], 16) - 20)
        b = max(0, int(hex_color[5:7], 16) - 20)
        return f"#{r:02x}{g:02x}{b:02x}"

# -----------------------------
# Styled Entry
# -----------------------------
def make_entry(parent, width=18):
    return tk.Entry(
        parent, width=width, bg=ENTRY_BG, fg=TEXT,
        insertbackground=PRIMARY, relief="flat",
        font=("Helvetica", 11),
        highlightthickness=1,
        highlightcolor=PRIMARY,
        highlightbackground=BORDER
    )

# -----------------------------
# Styled Treeview (Tables)
# -----------------------------
def make_table(parent, columns, labels, height=6):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("P.Treeview",
                    background=PANEL, foreground=TEXT,
                    rowheight=40, fieldbackground=PANEL,
                    font=("Helvetica", 10), borderwidth=0)
    style.configure("P.Treeview.Heading",
                    background=HEADER_BG, foreground=SUBTEXT,
                    font=("Helvetica", 10, "bold"), relief="flat")
    style.map("P.Treeview",
              background=[("selected", "#EEF2FF")],
              foreground=[("selected", PRIMARY)])

    tree = ttk.Treeview(parent, columns=columns, show="headings",
                        height=height, style="P.Treeview")
    for col, lbl in zip(columns, labels):
        tree.heading(col, text=lbl)
        tree.column(col, anchor="center", width=185)

    tree.tag_configure("even", background=PANEL)
    tree.tag_configure("odd",  background="#FAFCFF")
    tree.tag_configure("accepted", foreground=SUCCESS, font=("Helvetica", 10, "bold"))
    tree.tag_configure("rejected", foreground=SECONDARY)
    tree.tag_configure("pending",  foreground="#FFB547")

    sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    return tree, sb

# ============================================================
# CORE FUNCTIONS
# ============================================================

def refresh_stats():
    try:
        cursor.execute("SELECT COUNT(*) FROM Job_Posting WHERE status='approved'"); j = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Student");                             s = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Offer WHERE offer_status='accepted'"); p = cursor.fetchone()[0]
        
        stat_jobs.config(text=str(j))
        stat_students.config(text=str(s))
        stat_placed.config(text=str(p))
    except:
        pass

def view_jobs():
    cursor.execute("""
        SELECT jp.job_id, jp.role, c.company_name,
               CONCAT('₹ ', FORMAT(jp.salary, 0))
        FROM Job_Posting jp
        JOIN Company c ON jp.company_id = c.company_id
        WHERE jp.status = 'approved'
        ORDER BY jp.salary DESC
    """)
    job_table.delete(*job_table.get_children())
    for i, row in enumerate(cursor.fetchall()):
        job_table.insert("", tk.END, values=row, tags=("even" if i % 2 == 0 else "odd",))
    refresh_stats()

def on_job_click(event):
    selected = job_table.focus()
    if selected:
        values = job_table.item(selected, 'values')
        if values:
            job_entry.delete(0, tk.END)
            job_entry.insert(0, values[0]) 

def apply_job():
    sid = student_entry.get().strip()
    jid = job_entry.get().strip()
    if not sid or not jid or sid == "Student ID" or jid == "Job ID":
        messagebox.showwarning("Missing Fields", "Enter both Student ID and Job ID.")
        return
    try:
        cursor.execute("SELECT offer_id FROM Offer WHERE student_id=%s AND job_id=%s", (sid, jid))
        if cursor.fetchone():
            messagebox.showwarning("Already Applied", "You already applied for this job.")
            return
        cursor.execute(
            "INSERT INTO Offer (student_id, job_id, offer_status) VALUES (%s, %s, 'pending')",
            (sid, jid)
        )
        db.commit()
        messagebox.showinfo("Success", "Application submitted successfully!")
        view_applications() 
    except Exception as e:
        db.rollback()
        messagebox.showerror("DB Error", str(e))

def view_applications():
    sid = student_entry.get().strip()
    if not sid or sid == "Student ID":
        messagebox.showwarning("Missing Field", "Enter your Student ID first.")
        return
    cursor.execute("""
        SELECT o.offer_id, jp.role, c.company_name, o.offer_status
        FROM Offer o
        JOIN Job_Posting jp ON o.job_id = jp.job_id
        JOIN Company c      ON jp.company_id = c.company_id
        WHERE o.student_id = %s
        ORDER BY o.offer_id DESC
    """, (sid,))
    app_table.delete(*app_table.get_children())
    for row in cursor.fetchall():
        status = row[3]
        app_table.insert("", tk.END, values=row, tags=(status,))

def add_student():
    roll   = sid_entry.get().strip()
    name   = name_entry.get().strip()
    branch = branch_entry.get().strip()
    batch  = batch_entry.get().strip()
    cgpa   = cgpa_entry.get().strip()
    if not all([roll, name, branch, batch, cgpa]):
        messagebox.showwarning("Missing Fields", "Fill in all student fields.")
        return
    try:
        cursor.execute("""
            INSERT INTO Student (roll_number, name, branch, batch, cgpa, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (roll, name, branch, int(batch), float(cgpa), roll + "@mail.com"))
        db.commit()
        new_id = cursor.lastrowid
        
        for e in [sid_entry, name_entry, branch_entry, batch_entry, cgpa_entry]:
            e.delete(0, tk.END)
            
        student_entry.delete(0, tk.END)
        student_entry.insert(0, str(new_id))
        student_entry.config(fg=TEXT)
        refresh_stats()
        
        messagebox.showinfo("Success",
            f"Student '{name}' registered successfully!\n\n"
            f"Student ID : {new_id}\n"
            f"Your Student ID has been auto-filled!"
        )
    except Exception as e:
        db.rollback()
        messagebox.showerror("DB Error", str(e))


# ============================================================
# TRANSACTION FUNCTIONS
# ============================================================

def accept_offer_transaction():
    sid = student_entry.get().strip()
    oid = job_entry.get().strip()

    if not sid or not oid:
        messagebox.showwarning("Input Error", "Enter Student ID and Offer ID")
        return

    try:
        if db.in_transaction:
            db.rollback()

        db.start_transaction()

        # Accept selected offer
        cursor.execute(
            "UPDATE Offer SET offer_status='accepted' WHERE offer_id=%s",
            (oid,)
        )

        # Reject other pending offers
        cursor.execute(
            """
            UPDATE Offer
            SET offer_status='rejected'
            WHERE student_id=%s AND offer_id<>%s AND offer_status='pending'
            """,
            (sid, oid)
        )

        db.commit()
        messagebox.showinfo("Success", "Offer accepted. Others rejected.")

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", str(e))


def withdraw_applications_transaction():
    sid = student_entry.get().strip()

    if not sid:
        messagebox.showwarning("Input Error", "Enter Student ID")
        return

    try:
        if db.in_transaction:
            db.rollback()

        db.start_transaction()

        cursor.execute(
            "DELETE FROM Offer WHERE student_id=%s AND offer_status='pending'",
            (sid,)
        )

        # Logging (optional but good)
        cursor.execute(
            """
            INSERT INTO Placement_Log (student_id, log_message)
            VALUES (%s, 'Withdraw all applications')
            """,
            (sid,)
        )

        db.commit()
        messagebox.showinfo("Success", "All pending applications withdrawn.")

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", str(e))


def rollback_demo():
    sid = student_entry.get().strip()

    try:
        if db.in_transaction:
            db.rollback()

        db.start_transaction()

        cursor.execute(
            "UPDATE Offer SET offer_status='pending' WHERE student_id=%s",
            (sid,)
        )

        # INTENTIONAL rollback
        db.rollback()

        messagebox.showinfo("Rollback", "Transaction rolled back successfully.")

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", str(e))


def conflict_demo():
    oid = job_entry.get().strip()

    try:
        conn1 = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rohit123",
            database="internship_placement_db"
        )
        conn2 = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rohit123",
            database="internship_placement_db"
        )

        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        conn1.start_transaction()
        cur1.execute(
            "UPDATE Offer SET offer_status='accepted' WHERE offer_id=%s",
            (oid,)
        )

        conn2.start_transaction()
        messagebox.showinfo("Conflict", "Session 2 will wait (simulating lock)")

        cur2.execute(
            "UPDATE Offer SET offer_status='rejected' WHERE offer_id=%s",
            (oid,)
        )

        conn1.commit()
        conn2.commit()

        conn1.close()
        conn2.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ============================================================
# ROOT WINDOW
# ============================================================
root = tk.Tk()
root.title("Placement Portal")
root.geometry("1180x860")
root.minsize(1024, 768)
root.configure(bg=BG)

# ============================================================
# SIDEBAR
# ============================================================
sidebar = tk.Frame(root, bg=PANEL, width=240, highlightbackground=BORDER, highlightthickness=1)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Logo Area
logo_frame = tk.Frame(sidebar, bg=PANEL)
logo_frame.pack(fill="x", pady=30, padx=24)
tk.Label(logo_frame, text="▶", font=("Helvetica", 20), fg=SECONDARY, bg=PANEL).pack(side="left")
tk.Label(logo_frame, text=" Placement\n Portal", font=("Helvetica", 16, "bold"), fg=TEXT, bg=PANEL, justify="left").pack(side="left", padx=8)

# Navigation Links
for i, item in enumerate(["Dashboard", "Jobs", "Schedule", "Documents", "Statistics"]):
    c = PRIMARY if i == 0 else SUBTEXT
    f = ("Helvetica", 11, "bold") if i == 0 else ("Helvetica", 11)
    tk.Label(sidebar, text=f"   {item}", font=f, fg=c,
             bg=PANEL, anchor="w", padx=24, pady=14, cursor="hand2").pack(fill="x")

# ============================================================
# MAIN PANEL
# ============================================================
main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

# -- Top Bar --
topbar = tk.Frame(main, bg=BG, height=80)
topbar.pack(fill="x", padx=28, pady=10)
topbar.pack_propagate(False)

tk.Label(topbar, text="Dashboard",
         font=("Helvetica", 22, "bold"), fg=TEXT, bg=BG).pack(side="left", pady=20)

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg=TEXT)

for lbl, width in [("Student ID", 12), ("Job ID", 10)]:
    e = make_entry(topbar, width=width)
    e.config(fg=SUBTEXT)
    e.insert(0, lbl)
    e.bind("<FocusIn>", lambda event, entry=e, label=lbl: clear_placeholder(event, entry, label))
    e.pack(side="left", padx=(15, 0), ipady=8, pady=20)
    if lbl == "Student ID": student_entry = e
    else: job_entry = e

AnimButton(topbar, "Apply Now", command=apply_job, color=PRIMARY, width=12).pack(side="left", padx=10, pady=20)
AnimButton(topbar, "Fetch Apps",  command=view_applications, color=SECONDARY, width=12).pack(side="left", pady=20)
AnimButton(topbar, "Accept Offer TX", command=accept_offer_transaction, color=SUCCESS, width=14).pack(side="left", padx=5)
AnimButton(topbar, "Withdraw TX", command=withdraw_applications_transaction, color=SECONDARY, width=14).pack(side="left", padx=5)
AnimButton(topbar, "Rollback Demo", command=rollback_demo, color="#6C63FF", width=14).pack(side="left", padx=5)
AnimButton(topbar, "Conflict Demo", command=conflict_demo, color="#FF8C00", width=14).pack(side="left", padx=5)

# -- Scrollable Content --
outer_canvas = tk.Canvas(main, bg=BG, highlightthickness=0)
vscroll = ttk.Scrollbar(main, orient="vertical", command=outer_canvas.yview)
outer_canvas.configure(yscrollcommand=vscroll.set)
vscroll.pack(side="right", fill="y")
outer_canvas.pack(fill="both", expand=True)

content = tk.Frame(outer_canvas, bg=BG)
outer_canvas.create_window((0, 0), window=content, anchor="nw")
content.bind("<Configure>", lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all")))

def _on_mousewheel(event):
    if event.widget.winfo_class() == 'Treeview':
        return 
    if platform.system() == 'Darwin':
        outer_canvas.yview_scroll(int(-1 * event.delta), "units")
    else:
        outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

outer_canvas.bind_all("<MouseWheel>", _on_mousewheel)

PAD = {"padx": 28, "pady": 10}

# ============================================================
# STATS ROW
# ============================================================
stats_row = tk.Frame(content, bg=BG)
stats_row.pack(fill="x", padx=28, pady=(0, 10))

def create_stat_card(parent, title, accent_color):
    card = tk.Frame(parent, bg=PANEL, padx=20, pady=20, highlightbackground=BORDER, highlightthickness=1)
    card.pack(side="left", fill="x", expand=True, padx=(0, 15))
    tk.Label(card, text=title, font=("Helvetica", 11), fg=SUBTEXT, bg=PANEL, anchor="w").pack(fill="x")
    val_lbl = tk.Label(card, text="0", font=("Helvetica", 28, "bold"), fg=TEXT, bg=PANEL, anchor="w")
    val_lbl.pack(fill="x", pady=(5, 0))
    tk.Frame(card, bg=accent_color, height=4).pack(fill="x", pady=(10, 0))
    return val_lbl

stat_jobs     = create_stat_card(stats_row, "Active Jobs", PRIMARY)
stat_students = create_stat_card(stats_row, "Total Students", SECONDARY)
stat_placed   = create_stat_card(stats_row, "Offers Accepted", SUCCESS)

# ============================================================
# SECTION 1 — JOB LISTINGS
# ============================================================
s1 = tk.Frame(content, bg=BG)
s1.pack(fill="x", **PAD)

tk.Label(s1, text="Available Jobs", font=("Helvetica", 14, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(10, 8))

card1 = tk.Frame(s1, bg=PANEL, padx=2, pady=2, highlightbackground=BORDER, highlightthickness=1)
card1.pack(fill="x")

job_table, job_sb = make_table(card1,
    ("ID", "Role", "Company", "Salary"),
    ("Job ID", "Role", "Company", "Salary (₹)"), height=7)
job_table.pack(side="left", fill="both", expand=True)
job_sb.pack(side="right", fill="y")

job_table.bind("<ButtonRelease-1>", on_job_click)

# ============================================================
# SECTION 2 — MY APPLICATIONS & REGISTRATION
# ============================================================
s2 = tk.Frame(content, bg=BG)
s2.pack(fill="x", **PAD)

col_left = tk.Frame(s2, bg=BG)
col_left.pack(side="left", fill="both", expand=True, padx=(0, 15))

col_right = tk.Frame(s2, bg=BG)
col_right.pack(side="right", fill="y")

tk.Label(col_left, text="Application Status", font=("Helvetica", 14, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(10, 8))
card2 = tk.Frame(col_left, bg=PANEL, padx=2, pady=2, highlightbackground=BORDER, highlightthickness=1)
card2.pack(fill="both", expand=True)

app_table, app_sb = make_table(card2,
    ("OfferID", "Role", "Company", "Status"),
    ("Offer ID", "Role", "Company", "Status"), height=6)
app_table.pack(side="left", fill="both", expand=True)
app_sb.pack(side="right", fill="y")

tk.Label(col_right, text="New Candidate", font=("Helvetica", 14, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(10, 8))
card3 = tk.Frame(col_right, bg=PANEL, padx=24, pady=20, highlightbackground=BORDER, highlightthickness=1)
card3.pack(fill="y", expand=True)

_entries = {}
for label in ["Roll Number", "Full Name", "Branch", "Batch Year", "CGPA"]:
    tk.Label(card3, text=label, font=("Helvetica", 9, "bold"),
             fg=SUBTEXT, bg=PANEL, anchor="w").pack(fill="x", pady=(8, 2))
    e = make_entry(card3, width=22)
    e.pack(fill="x", ipady=6)
    _entries[label] = e

sid_entry    = _entries["Roll Number"]
name_entry   = _entries["Full Name"]
branch_entry = _entries["Branch"]
batch_entry  = _entries["Batch Year"]
cgpa_entry   = _entries["CGPA"]

AnimButton(card3, "Add Student", command=add_student, color=SUCCESS, width=20).pack(pady=(20, 0))

# ============================================================
# FOOTER
# ============================================================
tk.Label(content, text="Placement Management System v5.0", font=("Helvetica", 9), fg=SUBTEXT, bg=BG).pack(pady=(20, 40))

# ============================================================
# INIT
# ============================================================
view_jobs()
root.mainloop()