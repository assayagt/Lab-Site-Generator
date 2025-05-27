from src.DAL.DTOs.NewsRecord_dto import NewsRecord_dto


class News_repo:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_all(self):
        query = "SELECT * FROM news"
        results = self.db_manager.execute_query(query)
        return [self._row_to_news_record_dto(row) for row in results]

    def find_news_by_domain(self, domain):
        query = "SELECT * FROM  news WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_news_record_dto(row) for row in result]

    def save_news_record(self, news_record_dto: NewsRecord_dto):
        query = """
        INSERT INTO news (
            id, domain, text, link, date
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            domain = excluded.domain,
            text = excluded.text,
            link = excluded.link,
            date = excluded.date
        """
        params = (
            news_record_dto.id,
            news_record_dto.domain,
            news_record_dto.text,
            news_record_dto.link,
            news_record_dto.date
        )
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0

    def delete_notification(self, id):
        query = "DELETE FROM news WHERE id = ?"
        rows_affected = self.db_manager.execute_update(query, id)
        return rows_affected > 0

    def _row_to_news_record_dto(self, row):
        return NewsRecord_dto(
            domain=row['domain'],
            id=row['id'],
            text=row['text'],
            link=row['link'],
            date=row['date']
        )