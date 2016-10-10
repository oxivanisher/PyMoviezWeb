#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from pymoviezweb.utils import *
from pymoviezweb.database import db_session, Base


# movie class
class Movie(Base):
    __tablename__ = 'movies'

    # listAttributes = ['Medium', 'Genre', 'Director', 'Actor' ]

    id = Column(Integer, primary_key=True)

    Title = Column(String(255))
    Cover = Column(String(255))
    Country = Column(String(255))
    Loaned = Column(String(255))
    LoanDate = Column(String(255))
    Length = Column(String(255))
    URL = Column(String(255))
    MovieID = Column(String(255))
    MPAA = Column(String(255))
    PersonalRating = Column(String(255))
    PurchaseDate = Column(String(255))
    Seen = Column(String(255))
    Rating = Column(String(255))
    Status = Column(String(255))
    ReleaseDate = Column(String(255))
    Notes = Column(String(255))
    Position = Column(String(255))
    Location = Column(String(255))

    Year = Column(Integer)

    Plot = Column(UnicodeText) #MEDIUMTEXT

    # __table_args__ = (UniqueConstraint(network_handle, entry_name, name="handle_name_uc"), )

    def __init__(self, Title):
        self.log = logging.getLogger(__name__)
        self.log.debug("[Movie] Initializing Movie %s" % (Title))
        self.Title = Title

    def __repr__(self):
        return '<Movie %r>' % self.id

    # def get(self):
    #     return json.loads(self.cache_data)

    # def set(self, cache_data):
    #     self.cache_data = json.dumps(cache_data)

    # def age(self):
    #     return int(time.time()) - self.last_update
