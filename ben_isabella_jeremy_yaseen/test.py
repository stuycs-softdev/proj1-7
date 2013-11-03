#!/usr/local/bin/python
from models import *
import utils

if __name__ == '__main__':
    # Setup
    users = User()
    posts = Post()
    comms = Comment()

    # Creating users, note the date field
    u = users.insert(username="Ben", password="iamsilly")
    u2 = users.insert(username="Jeremy", password="YOLO")

    # Creating posts, note the date field
    p = u.add_post(title="Hello World", body="My first post",
            tags=["best","post","ever"])
    p2 = u2.add_post(title="Not a traditional title", body="I've posted before",
            tags=["original","stuff","bro"])

    # Adding comment to first post
    p.add_comment(user="Jeremy", text="this is stupid")
    u.vote_up(p.get_id())
    u2.vote_up(p.get_id())
    u.vote_up(p2.get_id())

    print "Getting comments from Jeremy..."
    for c in u2.get_comments():
        print c.text, ',', c.date

    print "\nGetting comments from Hello World post..."
    for c in p.get_comments():
        print c.text, ',', c.date

    print "\nGetting most popular posts..."
    for p in posts.get_most_voted():
        print "%s\n%s\n%s\nTags: %s, %s upvotes %s\n" % (p.title, p.user, p.body, ', '.join(p.tags), p.upvotes, p.date)

    print "\nGetting posts with tag 'original'..."
    for p in utils.search('original'):
        print "%s\n%s\n%s\n%s %s\n" % (p['title'], p['user'], p['body'], ', '.join(p['tags']), p['date'])

    # Cleaning up
    utils.clear_index()
    utils.index()
    users.remove_all()
    posts.remove_all()
    comms.remove_all()
