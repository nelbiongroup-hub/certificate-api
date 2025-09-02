import psycopg2
import os

DATABASE_URL = "postgresql://nelbion_db_user:FLeZq1VZpHRTXEoaBH5rlFkDAxYb0dd9@dpg-d2rc6qidbo4c73d4mcf0-a.frankfurt-postgres.render.com/nelbion_db" # Replace this!

def create_and_populate_db():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Create the certificates table with new 'summary' column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                cert_number VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                course VARCHAR(255),
                date VARCHAR(255),
                partner VARCHAR(255),
                portal VARCHAR(255),
                summary TEXT
            );
        ''')
        
        # Add certificate data, including a sample summary for each
        certificates_data = [
            ('RCCG-GSP-NA-2025-001', 'OKEICHE CHUKWUDI', 'Projection, Graphic Design, and Social Media Management.', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'CHUKWUDI demonstrated strong skills in Projection, Graphic Design, and Social Media Management. He was a very smart and eager learner who quickly grasped new concepts. As the leader of the team, he showed excellent leadership qualities and managed responsibilities without causing any stress.'),
            ('RCCG-GSP-NA-2025-002', 'ADANIKE MICHAEL', 'Video Production and Photography,and Editing', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'MICHAEL excelled in Video and Photo Taking as well as Editing. He showed great enthusiasm for learning and consistently worked on improving his skills. His commitment to growth was evident throughout the training.'),
            ('RCCG-GSP-NA-2025-003', 'EBHAJIE PRINCE', 'Content Creation, Projection, and Graphic Design.', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'PRINCE developed solid skills in Content Creation, Projection, and Graphic Design. He displayed a good foundation for learning and showed potential to grow further in the media field.'),
            ('RCCG-GSP-NA-2025-004', 'OTUMAGIE FAVOUR', 'Content Creation, Video Production, and Photography.', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'FAVOUR displayed strong interest in Content Creation, Video and Photo Taking, and Editing. She was very eager to learn and consistently engaged with the training, showing promising growth.'),
            ('RCCG-GSP-NA-2025-005', 'AGHO OSARUGUE', 'Content Creation.', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'OSARUGUE brought surprising yet impressive skills in Content Creation to the course. Her selection proved valuable, as she demonstrated natural ability and creative talent in her work.'),
            ('RCCG-GSP-NA-2025-006', 'OLOTHI ELOGHENE FAITH', 'Content Creation, Graphic Design, and Projection', 'SEPT 2025', 'RCCG Good Shepherd Parish', 'Nelbion Academy', 'ELOGHENE showed dedication and readiness to learn in Content Creation, Graphic Design, and Projection. She approached tasks with enthusiasm and demonstrated a strong willingness to improve her craft.'),
            ('NELB-2025-BL1-OO1', 'IGWE ONYEKACHI', 'Beginner’s Level 1', 'AUG 2025', None, 'Nelbion Academy', 'ONYEKACHI joined the program with significant challenges, including difficulty with reading and low self-esteem. While he did not participate in the full media training courses like the other students, special attention was given to help him build confidence, self-belief, and the foundations for future learning. Rather than focusing on technical media skills, his sessions were tailored to encourage participation, improve his ability to engage in group activities, and develop a sense of accomplishment. Through patience, guidance, and steady encouragement, he was able to complete the Beginner’s Level 1 program, which recognized his effort, determination, and progress. Awarding him the Beginner’s Level 1 Certificate was not only a mark of his growth but also a way of affirming his potential. This achievement served as a confidence booster, showing him that he is capable of learning, improving, and taking the first steps toward a brighter future.'),
        ]

        cursor.executemany('INSERT INTO certificates VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (cert_number) DO NOTHING', certificates_data)
        
        conn.commit()
        print("Database table created and populated with summaries successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_and_populate_db()