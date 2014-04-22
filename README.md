coffeespot
==========
Basic blog software, supporting much less than wordpress.

Installing:

    sudo apt-get install python python-virtualenv git
    virtualenv -p python2.7 coffeespot-env
    cd coffeespot-env
    source bin/activate
    git clone https://github.com/mintpeter/coffeespot.git
    cd coffeespot
    python setup.py develop

To serve, first create a development.ini.
Then, in the directory containing that file:

    source ../bin/activate
    pserve --reload development.ini

This is just for a development server. For further information on
deployment, [consult Pyramid's documentation](http://pyramid-cookbook.readthedocs.org/en/latest/deployment/).
