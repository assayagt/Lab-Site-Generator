from DTOs.Notification_dto import notification_dto

class NotificationRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_notifications_by_domain_email(self, domain, email):
        query = """
        SELECT * FROM notifications
        WHERE domain = ? AND recipient = ?
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_notification_dto(row) for row in results]
    
    def save_notification(self, notif_dto: notification_dto):
        query = """
        INSERT OR REPLACE INTO notifications(
        domain, id, recipient, subject, body, request_email, publication_id, isRead
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            notif_dto.domain,
            notif_dto.id,
            notif_dto.recipient,
            notif_dto.subject,
            notif_dto.body,
            notif_dto.request_email,
            notif_dto.publication_id,
            notif_dto.isRead
        )
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def delete_notification(self, domain, id):
        query = "DELETE FROM notifications WHERE domain = ? AND id = ?"
        rows_affected = self.db_manager.execute_update(query, (domain, id))
        return rows_affected > 0


    def _row_to_notification_dto(self,row):
        return notification_dto(
            domain=row['domain'],
            id=row['id'],
            recipient=row['recipient'],
            subject=row['subject'],
            body=row['body'],
            request_email=row['request_email'],
            publication_id=row['publication_id'],
            isRead=bool(row['isRead'])
        )