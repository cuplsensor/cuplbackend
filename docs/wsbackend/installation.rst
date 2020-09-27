Installation
=============
This tutorial assumes you have Git and Python 3 installed.

Install Prerequisites
-----------------------
One of the dependencies (Postgres library `Psycopg2 <https://www.psycopg.org/docs/install.html#install-from-source>`_)
should be built from source.

GCC Compiler
^^^^^^^^^^^^^
To install GCC on Debian, open a terminal window and type::

    $ sudo apt install build-essential

To check gcc is installed, type::

    $ gcc --version

Python Header Files
^^^^^^^^^^^^^^^^^^^^
To install the Python 3 header files type::

    $ sudo apt-get install python3-dev

Libpq-dev
^^^^^^^^^^
This To install libbq-dev type::

    $ sudo apt-get install libpq-dev

Clone the Repo
--------------------
First you will need to download wsbackend by cloning its Git
repository. Open a terminal window, browse to a folder of your choice and type::

    $ git clone https://github.com/websensor/wsbackend.git

The GitHub repository will be cloned to a folder named ``wsbackend``.
Open this by typing::

    $ cd wsbackend

Create a Virtual Environment
--------------------------------------
We will use `virtualbox <https://virtualenv.pypa.io/en/latest/>`_ to create a virtual
environment. This will isolate our wsbackend installation from the rest of the system.

First install virtualenv::

    $ sudo pip3 install virtualenv

Next create a virtual environment named ``wsbackend_env``::

    $ virtualenv wsbackend_env

Activate the Virtual Environment
---------------------------------
In order for ``pip`` to install dependencies into the virtual enviornment, you must activate it first with::

    $ source wsbackend_env/bin/activate

Install Dependencies
----------------------
wsbackend is dependent on a number of Python packages including `flask <https://palletsprojects.com/p/flask/>`_.
These are listed in `requirements.txt <https://github.com/websensor/wsbackend/blob/master/requirements.txt>`_.

To install all requirements, type::

    $ pip3 install -r requirements.txt

Define Environment Variables
-----------------------------

Auth0
^^^^^^


Install Gunicorn
-----------------
There are `many <https://flask.palletsprojects.com/en/1.1.x/deploying/>`_ options for
serving this Flask application. In this tutorial we will use Gunicorn. It is the easiest
to install::

    $ pip3 install gunicorn

Next run the application with::

    $ gunicorn main:app


