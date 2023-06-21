from sqlite_connector import SQLiteConnector


class DBWorker:
    def __init__(self):
        self.init_table()

    @staticmethod
    def get_top_users(limit: int = 5) -> list:
        with SQLiteConnector() as cur:
            result = cur.execute(f'SELECT * FROM users '
                                 f'ORDER BY top_score DESC LIMIT {limit}')
            result = result.fetchall()
            result = [{'name': user_name, 'score': score} for user_name, score in result]
            return result

    @staticmethod
    def record_user_score(user_name: str, score: int):
        with SQLiteConnector() as cur:
            top_score = cur.execute(
                'SELECT top_score FROM users WHERE name = ?',
                (user_name,)
            ).fetchone()
            if top_score and top_score[0] < score:
                cur.execute(
                    'UPDATE users SET top_score = ? WHERE name = ?',
                    (score, user_name)
                )
            elif not top_score:
                cur.execute(
                    'INSERT INTO users (name, top_score) VALUES (?, ?)',
                    (user_name, score)
                )

    @staticmethod
    def get_top_result(user_name: str):
        with SQLiteConnector() as cur:
            top_score = cur.execute(
                'SELECT top_score FROM users WHERE name = ?',
                (user_name,)
            ).fetchone()
            if top_score:
                return top_score[0]

    @staticmethod
    def init_table():
        with SQLiteConnector() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, top_score NUMBER)')
