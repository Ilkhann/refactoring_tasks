import smtplib

class DatabaseRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def save_order(self, order: dict) -> None:
        self.db.execute(f'INSERT INTO orders VALUES ({order})')

class EmailNotificationService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_order_confirmation(self, email: str, order_id: int, total: float) -> None:
        server = smtplib.SMTP(self.host, self.port)
        server.sendmail('shop@store.com', email, f'Order {order_id} confirmed. Total: {total}')
        server.quit()