import sqlalchemy
from sqlalchemy import select


class Database:
    def __init__(self, db_path: str):
        self.engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()
        self.courses_table = sqlalchemy.Table(
            'courses',
            self.metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('course_name', sqlalchemy.String),
            sqlalchemy.Column('date_range', sqlalchemy.String),
            sqlalchemy.Column('weekdays', sqlalchemy.String),
            sqlalchemy.Column('free_spots', sqlalchemy.Integer),
            sqlalchemy.Column('price', sqlalchemy.String),
        )
        self.metadata.create_all(self.engine)

    def check_course_exists(self, course_name: str, date_range: str, weekdays: str) -> bool:
        """
        Checks if a course with the given name, date range, and weekdays already exists in the database
        :param course_name: name of the swimming course
        :param date_range: date range of the course
        :param weekdays: weekdays of the course
        :return: Boolean indicating whether the course exists
        """
        query = select(self.courses_table).where(
            sqlalchemy.and_(
                self.courses_table.c.course_name == course_name,
                self.courses_table.c.date_range == date_range,
                self.courses_table.c.weekdays == weekdays,
            )
        )
        result = self.connection.execute(query).fetchone()
        return result is not None

    def insert_course(self, course_name: str, date_range: str, weekdays: str, free_spots: int, price: str) -> None:
        """
        Inserts a new course into the database
        :param course_name: name of the swimming course
        :param date_range: date range of the course
        :param weekdays: weekdays of the course
        :param free_spots: number of free spots for the course
        :param price: price of the course as string
        """
        insert_query = self.courses_table.insert().values(
            course_name=course_name,
            date_range=date_range,
            weekdays=weekdays,
            free_spots=free_spots,
            price=price,
        )
        self.connection.execute(insert_query)
        self.connection.commit()
