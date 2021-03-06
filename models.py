__author__ = 'Ognjen'
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from error import ValidationError
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import SearchQueryMixin

db = SQLAlchemy()
make_searchable()

#import logging
#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('sqlalchemy.engine.base').setLevel(logging.DEBUG)

class UserQuery(BaseQuery, SearchQueryMixin):
    pass

# table for representing user friendships
friendship = db.Table('friendship', db.metadata,
    db.Column("id1", db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    db.Column("id2", db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


class User(db.Model):
    query_class = UserQuery
    __tablename__ ='user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(20))
    last_name = db.Column(db.Unicode(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    search_vector = db.Column(TSVectorType('first_name', 'last_name'))
    friends = db.relationship("User", secondary=friendship,
                           primaryjoin=id==friendship.c.id1,
                           secondaryjoin=id==friendship.c.id2,
    )
    #def __init__(self, first_name, last_name, age, gender):
    #    self.first_name = first_name
    #    self.last_name = last_name
    #    self.age = age
    #    self.gender = gender

    def __repr__(self):
        age = str(self.age)
        if self.age < 0:
            age =  ''
        return ';'.join([str(self.id),self.first_name,self.last_name,str(age),self.gender])

    def to_json(self, full_info = False):
        if full_info:
            return{
                'id':self.id,
                'first_name':self.first_name,
                'last_name':self.last_name,
                'age':self.age,
                'gender':self.gender
            }
        else:
            return{
                'id':self.id,
                'first_name':self.first_name,
                'last_name':self.last_name
            }


    def from_json(self, json):
        if 'id' in json:
            self.id = json['id']
        if ('first_name' not in json) or (len(json['first_name'])>20):
            raise ValidationError('Invalid User first name')
        self.first_name = json['first_name']
        if 'last_name' in json:
            if not len(json['last_name'])>20:
                self.last_name = json['last_name']
            else:
                raise ValidationError('Invalid User last name')
        else:
            self.last_name=""
        if 'age' in json and json['age'] is not None and len(str(json['age'])):
            if str(json['age']).isdigit():
                 self.age = json['age']
            else:
                raise ValidationError('Invalid User age')
        else:
            self.age=None
        if 'gender' in json and json['gender'] in ['male', 'female', '', None]:
            self.gender = json['gender']
        elif not 'gender' in json:
            pass
        else:
            raise ValidationError('Invalid User gender')

    def from_csv(self, user_str): # copied from zad1, only for testing
        """ Read user from string formatted: id;first_name;last_name;age;gender;friend1_id,friend2_id...
        :param user_str: string to parse
        :returns: User or None if string format is invalid
        """
        fields = user_str.split(';')
        if len(fields) < 6:
            raise ValueError('too few parameters: ' + user_str)

        (id,first_name,last_name,age,gender,friends_str) = tuple([x.strip() for x in fields[:6]])
        friends = []
        if friends_str:
            friends = [x.strip() for x in friends_str.split(',')]
        # validate fields
        if id.isdigit() \
            and ((not age) or (age.isdigit())) \
            and (gender in ['male', 'female']) \
            and all(x.isdigit() for x in friends):

            # make object
            #self.id = int(id) # problem, next_id is not updated (screws up future inserts)
            self.first_name = first_name
            self.last_name = last_name
            if age:
                self.age = int(age)
            self.gender = gender
            #self.friends = set([int(friend) for friend in friends])
            return self
        else:
            raise ValueError('invalid values found in: ' + user_str)


# helper methods:

def add_friendship(id_1, id_2):
    if id_1 == id_2:
        raise ValidationError('Error: same user u1 and u2')
    try:      # TODO: is this atomic?

        #db.session.execute(friendship.insert(), [{'id1':id_1, 'id2':id_2}, {'id1':id_2, 'id2':id_1}])
        u1 = User.query.get(id_1)
        u2 = User.query.get(id_2)
        u1.friends.append(u2)
        u2.friends.append(u1)
        db.session.commit()
    except Exception as e:
        print 'add_friendship error: ' + str(e)


#@staticmethod
def remove_friendship(id_1, id_2):
    #db.session.execute(friendship.delete().where(db.and_(friendship.c.id1 == id_1, friendship.c.id2 == id_2)))
    #db.session.execute(friendship.delete().where(db.and_(friendship.c.id1 == id_2, friendship.c.id2 == id_1)))
    #db.session.commit()
    if id_1 == id_2:
        raise ValidationError('Error: same user u1 and u2')
    try:      # TODO: is this atomic?
        u1 = User.query.get(id_1)
        u2 = User.query.get(id_2)
        u1.friends.remove(u2)
        u2.friends.remove(u1)
        db.session.commit()
    except Exception as e:
        print 'remove_friendship error: ' + str(e)

def get_friends(id):
    #return db.engine.execute("select u.id, u.first_name, u.last_name from user as u, friendship where u.id = friendship.id2 and friendship.id1 = %(idd)s", idd=id).fetchall()
    return User.query.get_or_404(id).friends

def get_fof(id): #TODO: try to reduce to single sql query
    ret = []
    ret_ids = set()
    friends = User.query.get_or_404(id).friends
    friend_ids = [u.id for u in friends] + [id]
    for friend in friends:
        for fof in friend.friends:
            if fof.id not in ret_ids and fof.id not in friend_ids:
                ret_ids.add(fof.id)
                ret.append(fof.to_json())
                if len(ret) >= 100: return ret #limit results
    return ret

def get_suggested(id): #TODO: try to reduce to single sql query
    ret = []
    ret_ids = {}
    friends = User.query.get_or_404(id).friends
    friend_ids = [u.id for u in friends] + [id]
    for friend in friends:
        for fof in friend.friends:
            if len(ret) >= 100: break #limit results
            if fof.id not in friend_ids:
                if fof.id not in ret_ids:
                    ret_ids[fof.id] = 1
                elif ret_ids[fof.id] == 1:
                    ret.append(fof.to_json())
                    ret_ids[fof.id] += 1
                else:
                    ret_ids[fof.id] += 1
        else:
            continue
        break
    for f in ret:
        f['common'] = ret_ids[f['id']]

    return ret
