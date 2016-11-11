class TestCrestSqlHelper:
    @staticmethod
    def compare_db_to_crest(test, db, crest):
        for column in db.__table__.columns.keys():
            test.assertEqual(getattr(db, column), getattr(crest, column))
