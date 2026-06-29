"""
CivicHero AI - Database Module
Full SQLite schema with auth, issues, comments, and reset tokens
"""

import sqlite3
import os
import secrets
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "civichero.db")

DEPT_MAP = {
    "Pothole":     "PWD – Roads Division",
    "Water":       "Jal Nigam / Water Board",
    "Electricity": "DISCOM – Electricity Board",
    "Sewage":      "Municipal Corp – Sanitation",
    "Garbage":     "Sanitation Department",
    "Parks":       "Parks & Gardens Dept",
    "Construction":"Town Planning Authority",
    "Streetlight": "Municipal Lighting Division",
    "Other":       "Municipal Corporation",
}

# ── Connection ─────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ══════════════════════════════════════════════════
#  SCHEMA + SEED
# ══════════════════════════════════════════════════
def init_db():
    conn = get_db()
    cur  = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT    NOT NULL,
            email           TEXT    UNIQUE NOT NULL,
            password_hash   TEXT    NOT NULL,
            avatar          TEXT    DEFAULT '',
            bio             TEXT    DEFAULT '',
            phone           TEXT    DEFAULT '',
            points          INTEGER DEFAULT 0,
            reports         INTEGER DEFAULT 0,
            resolved        INTEGER DEFAULT 0,
            badge           TEXT    DEFAULT 'New Citizen',
            is_active       INTEGER DEFAULT 1,
            joined_at       TEXT    DEFAULT (datetime('now')),
            last_login      TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            token       TEXT    NOT NULL UNIQUE,
            expires_at  TEXT    NOT NULL,
            used        INTEGER DEFAULT 0,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS issues (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT    NOT NULL,
            description     TEXT    DEFAULT '',
            category        TEXT    DEFAULT 'Other',
            location        TEXT    NOT NULL,
            lat             REAL    DEFAULT 12.9716,
            lng             REAL    DEFAULT 77.5946,
            priority        TEXT    DEFAULT 'medium',
            status          TEXT    DEFAULT 'open',
            reporter        TEXT    DEFAULT 'Anonymous',
            image_path      TEXT,
            video_path      TEXT,
            ai_summary      TEXT    DEFAULT '',
            ai_severity     TEXT    DEFAULT 'medium',
            ai_department   TEXT    DEFAULT 'Municipal Corporation',
            ai_action       TEXT    DEFAULT '',
            ai_eta          TEXT    DEFAULT '3-5 days',
            ai_confidence   INTEGER DEFAULT 85,
            upvotes         INTEGER DEFAULT 0,
            views           INTEGER DEFAULT 0,
            verified        INTEGER DEFAULT 0,
            created_at      TEXT    DEFAULT (datetime('now')),
            updated_at      TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS timeline (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id   INTEGER NOT NULL,
            event      TEXT    NOT NULL,
            actor      TEXT    DEFAULT 'System',
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(issue_id) REFERENCES issues(id)
        );

        CREATE TABLE IF NOT EXISTS comments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id   INTEGER NOT NULL,
            author     TEXT    DEFAULT 'Anonymous',
            comment    TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(issue_id) REFERENCES issues(id)
        );
    """)

    # Seed demo user if no users
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        demo_hash = generate_password_hash("demo123")
        cur.execute("""
            INSERT INTO users (name,email,password_hash,points,reports,resolved,badge)
            VALUES (?,?,?,?,?,?,?)
        """, ("Aaryan Kumar", "demo@civichero.ai", demo_hash, 1840, 23, 8, "Community Champion"))

    # Seed issues if empty
    cur.execute("SELECT COUNT(*) FROM issues")
    if cur.fetchone()[0] == 0:
        _seed_issues(cur)

    conn.commit()
    conn.close()
    print("[DB] ✅ Initialized")


def _seed_issues(cur):
    seed = [
        ("Large pothole causing vehicle damage — 12th Main, Koramangala",
         "Multiple vehicles damaged tires due to a 3ft wide, 10-inch deep pothole. High accident risk near bus stop.",
         "Pothole", "12th Main, Koramangala, Bengaluru", 12.9352, 77.6245,
         "critical", "open", "Aaryan Kumar",
         "Critical pothole. Immediate road repair required to prevent accidents.", "critical",
         "PWD – Roads Division", "Deploy repair team urgently. Barricade area.", "24-48 hours", 92, 47, 156, 1, -3),

        ("Water pipe burst flooding HSR Layout main road",
         "Underground pipe burst. Water flowing for 36 hours causing road damage and traffic disruption.",
         "Water", "HSR Layout Sector 1, Bengaluru", 12.9116, 77.6389,
         "critical", "in_progress", "Priya Sharma",
         "Pipe burst confirmed. Severe water wastage and structural road damage.", "critical",
         "Jal Nigam / Water Board", "Deploy plumbing team. Shut valve at nearest junction.", "12-24 hours", 95, 62, 203, 1, -5),

        ("Garbage overflow — Ejipura, Bengaluru",
         "Municipal bins overflowing for 10+ days. Waste spreading to footpath. Rodents observed.",
         "Garbage", "Ejipura, Bengaluru", 12.9468, 77.6209,
         "high", "resolved", "Rahul Mishra",
         "Garbage collection failure resolved after community pressure campaign.", "medium",
         "Sanitation Department", "Increase collection frequency.", "Resolved", 88, 31, 89, 1, -10),

        ("Street lights out for 500m — Indiranagar 100ft Road",
         "15 consecutive streetlights non-functional. Multiple mugging incidents after dark.",
         "Streetlight", "100ft Road, Indiranagar, Bengaluru", 12.9784, 77.6408,
         "high", "in_progress", "Sunita Kaur",
         "Multiple streetlight outages creating severe safety hazard.", "high",
         "Municipal Lighting Division", "Emergency maintenance deployment required.", "48 hours", 90, 29, 112, 1, -5),

        ("Sewage overflow near Domlur flyover",
         "Sewage overflowing at Domlur flyover. Foul smell 200m radius. Health hazard near school.",
         "Sewage", "Domlur, Bengaluru", 12.9592, 77.6387,
         "critical", "open", "Dev Verma",
         "Sewage overflow is public health emergency. School within 100m.", "critical",
         "Municipal Corp – Sanitation", "Emergency drain cleaning needed immediately.", "24 hours", 96, 54, 178, 0, -1),

        ("Broken park benches — Cubbon Park",
         "Multiple benches broken, swing set collapsed. Children's play area unsafe.",
         "Parks", "Cubbon Park, Bengaluru", 12.9763, 77.5929,
         "medium", "open", "Farrukh Ahmed",
         "Infrastructure damage in public park. Safety hazard for children.", "medium",
         "Parks & Gardens Dept", "Schedule maintenance crew.", "5-7 days", 78, 18, 67, 0, -7),

        ("Unauthorized construction blocking road — Whitefield",
         "Construction debris on entire left lane of Whitefield Main Road. Severe traffic snarls.",
         "Construction", "Whitefield Main Road, Bengaluru", 12.9698, 77.7499,
         "high", "open", "Meena Devi",
         "Illegal construction obstruction causing major traffic disruption.", "high",
         "Town Planning Authority", "Issue notice. Clear debris within 24 hours.", "24-48 hours", 87, 38, 134, 1, -2),

        ("Water leakage wasting litres — MG Road",
         "Water pipe leaking from 5 days on MG Road near Trinity Circle. 10,000 litres wasted daily.",
         "Water", "MG Road, Trinity Circle, Bengaluru", 12.9748, 77.6094,
         "high", "open", "Kavita Rao",
         "Significant water wastage. Pipe leaking for 5 days. Environmental impact high.", "high",
         "Jal Nigam / Water Board", "Locate and repair leaking joint.", "48 hours", 91, 45, 167, 1, -4),

        ("Overflowing manhole causing accidents — BTM Layout",
         "Manhole cover missing and sewage overflowing. Two vehicles fell in yesterday.",
         "Sewage", "BTM Layout 2nd Stage, Bengaluru", 12.9166, 77.6101,
         "critical", "open", "Anjali Singh",
         "Missing manhole cover is life-threatening. Two accidents already reported.", "critical",
         "Municipal Corp – Sanitation", "Barricade immediately. Replace cover within 2 hours.", "Immediate", 98, 73, 289, 1, -1),

        ("Electricity transformer sparking — Jayanagar",
         "Transformer on Jayanagar 4th Block sparking. Power fluctuations affecting 50+ homes.",
         "Electricity", "Jayanagar 4th Block, Bengaluru", 12.9250, 77.5938,
         "critical", "resolved", "Pooja Reddy",
         "Sparking transformer resolved by emergency team. Transformer replaced.", "critical",
         "DISCOM – Electricity Board", "Emergency repair completed.", "Resolved", 97, 68, 234, 1, -8),
    ]

    for s in seed:
        days = s[-1]
        cur.execute("""
            INSERT INTO issues
              (title,description,category,location,lat,lng,priority,status,reporter,
               ai_summary,ai_severity,ai_department,ai_action,ai_eta,ai_confidence,
               upvotes,views,verified,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                    datetime('now', ? || ' days'),datetime('now', ? || ' days'))
        """, (*s[:-1], str(days), str(days)))

    cur.execute("SELECT id FROM issues")
    for (iid,) in cur.fetchall():
        cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,'Issue reported by citizen','Citizen')", (iid,))
        cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,'AI analysis complete — routed to department','Gemini AI')", (iid,))


# ══════════════════════════════════════════════════
#  AUTH FUNCTIONS
# ══════════════════════════════════════════════════
def create_user(name, email, password_hash):
    try:
        conn = get_db()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO users (name,email,password_hash) VALUES (?,?,?)
        """, (name, email, password_hash))
        user_id = cur.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND is_active=1", (email.lower(),))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def update_user_password(user_id, password_hash):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE users SET password_hash=? WHERE id=?", (password_hash, user_id))
    conn.commit()
    conn.close()


def create_reset_token(user_id):
    token      = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cur  = conn.cursor()
    # Invalidate old tokens for this user
    cur.execute("UPDATE password_reset_tokens SET used=1 WHERE user_id=?", (user_id,))
    cur.execute("""
        INSERT INTO password_reset_tokens (user_id,token,expires_at) VALUES (?,?,?)
    """, (user_id, token, expires_at))
    conn.commit()
    conn.close()
    return token


def verify_reset_token(token):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        SELECT user_id, expires_at, used FROM password_reset_tokens WHERE token=?
    """, (token,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    r = dict(row)
    if r["used"]:
        return None
    if datetime.utcnow() > datetime.strptime(r["expires_at"], "%Y-%m-%d %H:%M:%S"):
        return None
    return r["user_id"]


def mark_token_used(token):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE password_reset_tokens SET used=1 WHERE token=?", (token,))
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════
#  ISSUE FUNCTIONS
# ══════════════════════════════════════════════════
def add_issue(title, description, category, location, lat, lng, priority,
              reporter, image_path, video_path, ai_summary, ai_severity,
              ai_department, ai_action, ai_eta, ai_confidence, status="open"):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO issues
          (title,description,category,location,lat,lng,priority,status,reporter,
           image_path,video_path,ai_summary,ai_severity,ai_department,
           ai_action,ai_eta,ai_confidence)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (title, description, category, location, lat, lng, priority, status, reporter,
          image_path, video_path, ai_summary, ai_severity, ai_department,
          ai_action, ai_eta, ai_confidence))
    issue_id = cur.lastrowid
    cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,'Issue reported','Citizen')", (issue_id,))
    cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,'AI analysis complete — routed to department','Gemini AI')", (issue_id,))
    cur.execute("UPDATE users SET points=points+50, reports=reports+1 WHERE name=?", (reporter,))
    conn.commit()
    conn.close()
    return issue_id


def get_all_issues(limit=None):
    conn = get_db()
    cur  = conn.cursor()
    sql  = "SELECT * FROM issues ORDER BY created_at DESC"
    cur.execute(sql + (" LIMIT ?" if limit else ""), (limit,) if limit else ())
    rows = cur.fetchall()
    conn.close()
    return rows


def get_issue_by_id(issue_id):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE issues SET views=views+1 WHERE id=?", (issue_id,))
    conn.commit()
    cur.execute("SELECT * FROM issues WHERE id=?", (issue_id,))
    issue = cur.fetchone()
    cur.execute("SELECT * FROM timeline WHERE issue_id=? ORDER BY created_at ASC", (issue_id,))
    timeline = cur.fetchall()
    conn.close()
    return {"issue": issue, "timeline": timeline} if issue else None


def upvote_issue(issue_id):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE issues SET upvotes=upvotes+1 WHERE id=?", (issue_id,))
    cur.execute("SELECT upvotes FROM issues WHERE id=?", (issue_id,))
    count = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return count


def update_issue_status(issue_id, new_status):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE issues SET status=?,updated_at=datetime('now') WHERE id=?", (new_status, issue_id))
    cur.execute("SELECT reporter FROM issues WHERE id=?", (issue_id,))
    row = cur.fetchone()
    if row and new_status == "resolved":
        cur.execute("UPDATE users SET points=points+100, resolved=resolved+1 WHERE name=?", (row[0],))
    cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,?,'Admin')",
                (issue_id, f"Status changed to {new_status.replace('_',' ').title()}"))
    conn.commit()
    conn.close()


def add_comment(issue_id, author, comment):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("INSERT INTO comments (issue_id,author,comment) VALUES (?,?,?)", (issue_id, author, comment))
    cur.execute("INSERT INTO timeline (issue_id,event,actor) VALUES (?,?,'Citizen')",
                (issue_id, f"Comment added by {author}"))
    conn.commit()
    conn.close()


def get_comments(issue_id):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM comments WHERE issue_id=? ORDER BY created_at ASC", (issue_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_leaderboard(limit=10):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY points DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def search_issues(q):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""SELECT * FROM issues WHERE title LIKE ? OR description LIKE ? OR location LIKE ?
                   ORDER BY created_at DESC""",
                (f"%{q}%", f"%{q}%", f"%{q}%"))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_issues_by_category(category):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM issues WHERE category=? ORDER BY created_at DESC", (category,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM issues"); total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM issues WHERE status='resolved'"); resolved = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM issues WHERE status='open'"); open_c = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM issues WHERE status='in_progress'"); in_progress = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM issues WHERE priority='critical' AND status!='resolved'"); critical = cur.fetchone()[0]
    cur.execute("SELECT category, COUNT(*) as cnt FROM issues GROUP BY category ORDER BY cnt DESC")
    by_cat = [dict(r) for r in cur.fetchall()]
    cur.execute("""SELECT ai_department as ward, COUNT(*) as total,
                   SUM(CASE WHEN status='resolved' THEN 1 ELSE 0 END) as resolved
                   FROM issues GROUP BY ai_department ORDER BY total DESC LIMIT 5""")
    by_dept = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT COALESCE(SUM(upvotes),0) FROM issues"); total_upvotes = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(views),0) FROM issues"); total_views = cur.fetchone()[0]
    conn.close()
    return {
        "total": total, "resolved": resolved, "open": open_c,
        "in_progress": in_progress, "critical": critical,
        "resolution_rate": round((resolved/total*100) if total else 0, 1),
        "ai_accuracy": 92,
        "by_category": by_cat, "by_department": by_dept,
        "total_upvotes": total_upvotes, "total_views": total_views,
    }


def get_monthly_trends():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        SELECT strftime('%Y-%m', created_at) as month,
               COUNT(*) as total,
               SUM(CASE WHEN status='resolved' THEN 1 ELSE 0 END) as resolved
        FROM issues GROUP BY month ORDER BY month DESC LIMIT 6
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return list(reversed(rows))
