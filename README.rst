.. image:: https://circleci.com/gh/andela/learning_map_api.svg?style=shield
    :target: https://circleci.com/gh/andela/learning_map_api

C.A.L.M
=======

The Collective Andela Learning Map (C.A.L.M) server side implementation.

Contributions
-------------

Contributions should adhere to the guidelines in the
`Engineering Playbook <https://github.com/andela/engineering-playbook/wiki/Conventions>`_.

Development setup
-----------------

- Clone this repo and navigate into the project's directory

  .. code-block:: console

     $ git clone https://github.com/andela/learning_map_api && cd learning_map_api

- Create a ``python3`` virtual environment for the project and activate it.

  - To install ``python3`` on OSX you can
    `follow this <http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/>`_

  - To install the virtual environment wrapper ``mkvirtualenv`` you can
    `follow this <https://jamie.curle.io/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x>`_.

  .. code-block:: console

     $ mkvirtualenv --py=python3 learning_map_api

- Install the project's requirements

  .. code-block:: console

     $ pip install -r requirements.txt

- Copy ``.env.sample`` into ``.env`` in the ``api`` folder of the project.
  You should adjust it according to your own local settings. To set up
  ``postgres`` database locally you can
  `follow this <http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/>`_.

- Run the app

  .. code-block:: console

     $ gunicorn main:app

- The app should now be available from your browser at ``http://127.0.0.1:8000``
