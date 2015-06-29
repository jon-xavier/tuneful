import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine, session

class Song(Base):
    __tablename__ = "songs"
    
    id=Column(Integer, primary_key=True)
    file=Column(Integer, ForeignKey('files.id'), nullable=False)
    
    def as_dictionary(self):
        file_dict=session.query(File).get(self.id).as_dictionary()
        song= {
            "id": self.id,
            "file": file_dict
        }
        return song
    
class File(Base):
    __tablename__ = "files"
    
    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    song= relationship("Song", uselist=False, backref="song")
    
    def as_dictionary(self):
        file= {
            "id": self.id,
            "name": self.name
        }
        return file
    