from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@localhost:5432/project_tracker')

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))

    def __repr__(self):
        return "<Project(id = '{0}', title = '{1}')>".format(self.project_id, self.title)


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    description = Column(String(length=50))

    project = relationship("Project")

    def __repr__(self):
        return "<Task(description = '{0}')>".format(self.description)

Base.metadata.create_all(engine)

def create_session():
    session = sessionmaker(bind=engine)
    return session()

#


session = create_session()
clean_house = Project(title = "Clean the house")
session.add(clean_house)
session.commit()

clean_bedroom = Task(description= "Clean bedroom", project_id=clean_house.project_id)
session.add(clean_bedroom)
session.commit()