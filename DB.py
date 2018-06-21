from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import uuid

Base = declarative_base()
engine = create_engine('sqlite:///desafiogeru.db', echo=True)

DBsession = sessionmaker(bind=engine)
dbsession = DBsession()


class SessionID(Base):
    __tablename__ = 'sessionID'
    id = Column('id', String, primary_key=True)
    user_agent = Column('user_agent', String)


class Accesses(Base):
    __tablename__ = 'accesses'
    id = Column(String, ForeignKey('sessionID.id'))
    access_id = relationship(SessionID)
    table_id = Column('id_real', Integer, primary_key=True,
                      autoincrement=True)
    page = Column('page', String)
    date = Column('date', String)
    time = Column('time', String)


# poderia ter usado os tipos do datetime, mas sqlite n tem suporte
Base.metadata.create_all(engine)


def session_add(request):
    Q = dbsession.query(SessionID.id).filter(
        SessionID.user_agent == request.user_agent).first()
    # no primeiro acesso,  eu registro o identificador unico da sessao
    if Q is None:
        request.session[request.user_agent] = str(uuid.uuid4())
        print(request.user_agent)
        s = SessionID(id=request.session[request.user_agent],
                      user_agent=request.user_agent)
        dbsession.add(s)
        dbsession.commit()
    # procuro o id da sessao e adiciono a um acesso
    s_id = dbsession.query(SessionID.id).filter(
        request.user_agent == SessionID.user_agent).first()
    ac = Accesses(id=s_id[0],
                  page=request.url,
                  date=datetime.datetime.now().strftime('%d/%m/%Y'),
                  time=datetime.datetime.now().strftime('%H:%M:%S'))
    dbsession.add(ac)
    dbsession.commit()
