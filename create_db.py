import sqlite3

def create_and_populate_db():
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()

    # Create the certificates table with new 'summary' column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            cert_number TEXT NOT NULL,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            date TEXT NOT NULL,
            partner TEXT,
            portal TEXT NOT NULL,
            summary TEXT, -- New column for performance summary
            PRIMARY KEY (cert_number, portal)
        )
    ''')

    # Add certificate data, including a sample summary for each
    certificates_data = [
        ('NA-GSP-25-001', 'John Doe', 'Media Crash Training', 'Aug 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'John demonstrated excellent skills in media production and performed exceptionally well in the practical assessment.'),
        ('NA-GSP-25-002', 'Mary Johnson', 'Projection & Social Media', 'Aug 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'Mary showed great proficiency in social media strategy and excelled in her final project presentation.'),
        ('NA-GSP-25-003', 'Jane Smith', 'Web Development Fundamentals', 'Sep 2025', None, 'Nelbion Academy', 'Jane has a strong grasp of HTML, CSS, and JavaScript. She actively participated in all coding challenges and completed her coursework ahead of schedule.'),
    ]

    cursor.executemany('INSERT OR IGNORE INTO certificates VALUES (?, ?, ?, ?, ?, ?, ?)', certificates_data)

    conn.commit()
    conn.close()
    print("Database 'certificates.db' created and populated with summaries successfully!")

if __name__ == '__main__':
    create_and_populate_db()