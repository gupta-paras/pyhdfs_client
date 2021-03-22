# pyhdfs-client : Powerful HDFS Client for python

[![https://pypi.python.org/pypi/pyhdfs_client](https://img.shields.io/pypi/v/pyhdfs_client.svg)](https://pypi.org/project/pyhdfs-client)

## Why it's powerful?

Native hdfs client offers much better performance than webhdfs clients. However calling native client for hadoop operations have an additional overhead of starting jvm. pyhdfs-client brings the performance of native hdfs client without any overhead of starting jvm on every command execution.
<br>
<br>


## Features<hr>
- HDFS client for python
- Easy to integrate with python applications
- Better Performance than webhdfs clients
- Provide native hadoop client performance without any overhead

### New in 0.1.2 <hr>
- Added Support for UNIX

## Installation
```
pip install pyhdfs-client
```
 Requirements:  hadoop binaries and py4j installed<br><br>
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



## Contribution 
- Any contribution for enhancements and bug fixes is welcome.


## Credits<hr>
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.