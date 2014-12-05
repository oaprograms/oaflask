__author__ = 'Ognjen'
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

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

    def to_json(self):
        return{
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'age':self.age,
            'gender':self.gender,
            'friends':None
        }

    def from_json(self, json):
        try: #TODO: finish this
            id = json['id']
            first_name = json['first_name']
            last_name = json['last_name']
            age = json['age']
            gender = json['gender']
        except:
            pass # no required parameters

    #def get_url(self):
    #    return url_for('api.get_user', id=self.id, _external=True)

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
            self.id = int(id)
            self.first_name = first_name
            self.last_name = last_name
            if age:
                self.age = int(age)
            self.gender = gender
            #self.friends = set([int(friend) for friend in friends])
            return self
        else:
            raise ValueError('invalid values found in: ' + user_str)