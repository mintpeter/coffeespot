import os
import sys
import transaction
import tempfile
import subprocess

import yaml

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings

from ..models import DBSession, Posts, Categories, Base

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <command> [args]\n'
          'commands: new_post edit_post delete_post\n'
          'example: %s development.ini new_post\n'
          'example: %s development.ini edit_post 1' % (cmd, cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) < 3:
        usage(argv)
    elif argv[2] not in ['view_post', 'new_post', 'edit_post', 'delete_post']:
        usage(argv)
    elif argv[2] in ['edit_post', 'delete_post', 'view_post'] and\
        len(argv) < 4:
        usage(argv)
    else:
        config_uri = argv[1]
        engine = engine_from_config(get_appsettings(config_uri))
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine

        EDITOR = os.environ.get('EDITOR', 'vim')

        arg = argv[2]
        if arg == 'view_post':
            post_id = argv[3]
            post = DBSession.query(Posts).filter(Posts.id == post_id).first()
            print('%s \n %s' % (post.title, post.post))
        elif arg == 'new_post':
            categories = DBSession.query(Categories).all()
            category_list = ""
            for category in categories:
                category_list += " # {:2d} | {:s}\n".format(category.id,
                                                            category.name)
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                msg = \
""" # Type the post in the uncommented area, then save and quit.
 # 
 # Available categories include:
 # ID | NAME
{:s} #
title:
category_id:
,,,,,,,,,,
Here is the post.""".format("".join(category_list))
                temp.write(msg)
                temp.close()

                if subprocess.call([EDITOR, temp.name]) != 0:
                    raise IOError("%s did not save correctly" % temp.name)
                with open(temp.name) as f:
                    split_file = f.read().split(",,,,,,,,,,,")
                    headers = yaml.load(split_file[0])
                    post_post = split_file[1]
            required_headers = {'title', 'category_id'}
            if headers.viewkeys() & required_headers and len(post_post) > 0:
                post_title = headers['title']
                post_categoryid = headers['category_id']
                post = Posts(post_title,
                             1,
                             post_categoryid,
                             post_post)
                with transaction.manager:
                    DBSession.add(post)
                print 'Post successfully added.'
        else:
            print('Not ready yet.')


