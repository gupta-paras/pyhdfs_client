# pyhdfs-client

[![https://pypi.python.org/pypi/pyhdfs_client](https://img.shields.io/pypi/v/pyhdfs_client.svg)](https://pypi.org/project/pyhdfs-client)
### A py4j based hdfs client for python providing native hdfs CLI performance.
<br>

## Features<hr>
- Easy to integrate with python applications
- No extra overhead to start HDFS client on every call
- Native HDFS client performance

### New in 0.1.2 <hr>
- Added Support for UNIX

## Sample Usage<hr>
```
>>> from pyhdfs_client.pyhdfs_client import HDFSClient
>>> hdfs_client = HDFSClient()
>>> ret, out, err = hdfs_client.run(['-ls', '/'])
>>> print(out)
Found 1 items
drwxr-xr-x   - gp supergroup          0 2021-03-21 01:10 /f1
>>> hdfs_client.stop() # to terminate hdfs client
```

## Credits<hr>
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.