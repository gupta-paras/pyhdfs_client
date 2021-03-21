=============
pyhdfs-client
=============


.. image:: https://img.shields.io/pypi/v/pyhdfs_client.svg
        :target: https://pypi.python.org/pypi/pyhdfs_client

.. image:: https://img.shields.io/travis/gupta-paras/pyhdfs_client.svg
        :target: https://travis-ci.com/gupta-paras/pyhdfs_client

.. image:: https://readthedocs.org/projects/pyhdfs-client/badge/?version=latest
        :target: https://pyhdfs-client.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/gupta-paras/pyhdfs_client/shield.svg
     :target: https://pyup.io/repos/github/gupta-paras/pyhdfs_client/
     :alt: Updates



A py4j based hdfs client for python for native hdfs CLI performance.

Usage Example: 
- set java_home and hadoop_home

from pyhdfs_client.pyhdfs_client import HDFSClient

hdfs_client = HDFSClient()

hdfs_client.run(['-ls', '/folder1'])

* Free software: MIT license
* Documentation: https://pyhdfs-client.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
