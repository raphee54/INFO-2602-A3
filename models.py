from sqlalchemy import Integer, Column, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
import ast

from A_3.app import db

class Anime(db.Model):
    __tablename__='anime_programmes'

    anime_id=Column(Integer, primary_key=True)
    name=Column(String(100))
    genre=Column(String(120))
    type=Column(String(20))
    episodes=Column(String(10))
    rating=Column(String(5))#rating=Column(Float)
    members=Column(Integer)

    def fromJSON(self, json_rec):
        if 'anime_id' in json_rec:
            self.anime_id = json_rec['anime_id']
        else:
            raise Exception('The name field is required')

        self.name = json_rec['name'] if 'name' in json_rec else ''
        self.genre = json_rec['genre'] if 'genre' in json_rec else ''
        self.type = json_rec['type'] if 'type' in json_rec else ''
        self.episodes = json_rec['episodes'] if 'episodes' in json_rec else ''
        self.rating = json_rec['rating'] if 'rating' in json_rec else 0.0
        self.members = json_rec['members'] if 'members' in json_rec else 0

    def toDict(self):
            return {
            'anime_id': self.anime_id,
            'name': self.name,
            'genre':self.genre,
            'type':self.type,
            'episodes':self.episodes,
            'rating':self.rating,
            'members':self.members
        }    


def load_pkfile_into_table(target, connection, **kw):
    import json
    import csv
    with open('anime_small.csv','rU') as csv_file:
        csv_data = csv.DictReader(csv_file, fieldnames=("anime_id","name","genre","type","episodes","rating","members"))
        anime_list = []
        count = 0
        for row in csv_data:
            if count != 0:
                frame = {
                    "anime_id": '',
                    'name' : '',
                    "genre": '',
                    "type": '',   
                    "episodes": '',
                    "rating": '',
                    "members": ''
                }
                frame['anime_id'] = int(row['anime_id'])
                frame['name'] = row['name']
                frame['genre'] = row['genre']
                frame['type'] = row['type']
                frame['episodes'] = row['episodes']
                frame['rating'] = row['rating']
                frame['members'] = int(row['members'])
                anime_list.append(frame)
            else:
                count = 1
        for rec in anime_list:
            a = Anime()
            a.fromJSON(rec)
            db.session.add(a)
        db.session.commit()


listen(Anime.__table__, 'after_create', load_pkfile_into_table)
