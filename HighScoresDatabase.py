import sqlite3


class HighScoresDB:
    def __init__(self, name):
        self.conn = sqlite3.connect(f"{name}")
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute("""CREATE TABLE players (
                            name text,
                            score integer
                        )          
        """)

        self.conn.commit()
        self.conn.close()

    def all_records(self, asc_order):
        """Returns list of all records from the database, order by score asc or desc"""
        if asc_order:
            self.c.execute("SELECT ROWID, name, score FROM players ORDER BY score ASC")
        else:
            self.c.execute("SELECT ROWID, name, score FROM players ORDER BY score DESC")

        records = self.c.fetchall()
        self.conn.commit()

        return records

    def delete_score(self, record):
        """Deletes a record from the database with given player name"""
        self.c.execute(f"DELETE FROM players WHERE ROWID='{record[0]}'")
        self.conn.commit()

    def find_min_score(self):
        """Finds a minimal score and returns it with ID"""
        self.c.execute("SELECT ROWID, MIN(score) FROM players")
        record = self.c.fetchall()

        return record[0]

    def add_record(self, name, score):
        """Adds record to the database (Keeps only 5 records there)"""
        if len(self.all_records(False)) < 5:
            if self.all_records(False)[4] < score:
                self.c.execute(f"INSERT INTO players VALUES (:name, :score)",
                          {
                            "name": name,
                            "score": score,
                          }
                               )
                self.conn.commit()
        else:
            min_score_record = self.find_min_score()
            self.delete_score(min_score_record)

            self.c.execute(f"INSERT INTO players VALUES (:name, :score)",
                           {
                               "name": name,
                               "score": score,
                           }
                        )
            self.conn.commit()













