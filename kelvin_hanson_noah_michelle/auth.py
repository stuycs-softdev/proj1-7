#!usr/bin/python

from pymongo import MongoClient

#client = MongoClient('db.stuycs.org')
#client.authenticate('softdev','softdev')
client = MongoClient()
db = client.KMNH
users = db.users
posts = db.posts

def addUser(usr,pwd, admin=False):
    if(usr==None or pwd==None):
        return False
    if users.find({'usr':usr}).count() == 0:
        users.insert({'usr':usr,'pwd':pwd, 'admin':admin})
        return True
    else:
        return False

def auth(usr,pwd):
    if(usr==None or pwd==None):
        return False
    if users.find({'usr':usr}).count() == 0:
        return False
    if users.find_one({'usr':usr})['pwd'] == pwd:
        return True
    return False

def reset(usr, oldpwd, newpwd):
    if auth(usr, oldpwd) == False and newpwd != None:
        users.find_one({'usr':usr}).upsert({'pwd':newpwd})
        return True
    return False

def isAdmin(usr):
    if usr == None: return False
    return users.find_one({'usr':usr})['admin']

if(__name__ == "__main__"):
    
    print addUser("user", "password")
    print "%s (true)"%auth('user','password')
    print "%s (false)"%auth('user','asdf')
    print "%s (false)"%auth('asdf','asdf')
