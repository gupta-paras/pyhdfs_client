from src.hdfs_client import HDFSClient
import re
import os

hdfs_client = HDFSClient()

while True:
    command = input("HDFS-SHELL>")
    if command.strip().lower() == 'exit':
        break
    splitted = re.split("\s+", command)
    if len(splitted) > 1 and splitted[0] == 'hdfs' and splitted[1] == 'dfs':
        print(hdfs_client.dfs_execute(splitted[2:]))
    else:
        os.system(command)

print("Repl Exitted")