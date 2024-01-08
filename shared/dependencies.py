from shared.dbhandler import SessionLocal


def get_db():
    """Create db connection.
    :return: db connection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
