from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, PickleType
from sqlalchemy import create_engine, Boolean, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from hashlib import md5

engine = create_engine("sqlite:///mooc.db", echo=True)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


friendships = Table("friendships", Base.metadata,
	Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('request_status', Boolean)
)

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String(1000), nullable=False, unique=True)
	nickname = Column(String(64), nullable=True, unique=True)
	password = Column(String(1000), nullable=False)
	about_me = Column(String(600), nullable=True)
	last_seen = Column(DateTime)
	friends = relationship('User',
                               secondary=friendships,
                               primaryjoin=id== friendships.c.user_id,
                               secondaryjoin=id==friendships.c.friend_id,
                               backref="users"
    )

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)


class BookmarkedCourse(Base):
	__tablename__ = "bookmarkedcourses"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	course_id = Column(String(500), ForeignKey('courses.id'))

	user = relationship("User", backref=backref("bookmarkedcourses", order_by=id))
	course = relationship("Course", backref=backref("bookmarkedcourses", order_by=id))


class Course(Base):
	__tablename__ = "courses"

	id = Column(Integer, primary_key=True)
	course_shortname = Column(String(200), nullable=False)
	course_name = Column(String(500), nullable=False)
	course_icon = Column(String(1000))
	course_language = Column(String(200))
	course_instructor = Column(String(90), nullable=True)
	course_format = Column(String(10000), nullable=True)
	course_workload = Column(String(1000), nullable=True)
	course_workload_max = Column(Integer, nullable=True)
	course_workload_min = Column(Integer, nullable=True)
	course_prerequisites = Column(String(1000), nullable=True)
	course_description = Column(String(10000), nullable=True)
	course_categories = relationship("CourseCategory", backref="course")



class Term(Base):
	__tablename__ = "terms"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
	course_link = Column(String(1000), nullable=True)
	duration =  Column(Integer, nullable=True)
	startDay =  Column(Integer, nullable=True)
	startMonth =  Column(Integer, nullable=True)
	startYear =  Column(Integer, nullable=True)	

	course_association = relationship("Course", backref=backref("terms", order_by=id))	


class Category(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True, nullable=False)
	category_name = Column(String(500), nullable=False)
	category_description = Column(String(5000), nullable=True)

class CourseCategory(Base):
	__tablename__ = "course_categories"

	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
	course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

	course_assoc = relationship("Course", backref=backref("course_category_names", order_by=id))

class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
	rating = Column(Integer, nullable=True)

	user = relationship("User", backref=backref("ratings", order_by=id))
	course = relationship("Course", backref=backref("ratings", order_by=id))

class Review(Base):
	__tablename__ = "reviews"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	review = Column(String(10000), nullable=True)

	user = relationship("User", backref=backref("reviews", order_by=id))
	course = relationship("Course", backref=backref("reviews", order_by=id))

class Group(Base):
	__tablename__ = "groups"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	group_name = Column(String(10000), nullable=False)

	user = relationship("User", backref=backref("groups", order_by=id))
	course = relationship("Course", backref=backref("groups", order_by=id))
	
def main():
	pass


if __name__ == "__main__":
    main()