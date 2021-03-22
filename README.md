# pyhdfs-client

![https://pypi.python.org/pypi/pyhdfs_client](https://img.shields.io/pypi/v/pyhdfs_client.svg)
![https://pypi.python.org/pypi/pyhdfs_client](https://img.shields.io/travis/gupta-paras/pyhdfs_client.svg)
![https://pyhdfs-client.readthedocs.io/en/latest/?version=latest](https://readthedocs.org/projects/pyhdfs-client/badge/?version=latest)
![https://pyup.io/repos/github/gupta-paras/pyhdfs_client/](https://pyup.io/repos/github/gupta-paras/pyhdfs_client/shield.svg)

### A py4j based hdfs client for python providing native hdfs CLI performance.
<br>

## Features<hr>
- Easy to integrate with python applications
- Native HDFS client performance

## Sample Usage<hr>
```
>>> from pyhdfs_client.pyhdfs_client import HDFSClient
>>> hdfs_client = HDFSClient()
>>> ret, out, err = hdfs_client.run(['-ls', '/'])
>>> print(out)
Found 1 items
drwxr-xr-x   - gp supergroup          0 2021-03-21 01:10 /f1
```

## Credits<hr>
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.