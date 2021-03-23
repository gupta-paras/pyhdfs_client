"""Main module."""
import os
import re
import time
import sys
import shutil
import psutil

from py4j.java_gateway import launch_gateway, JavaGateway, GatewayParameters, CallbackServerParameters, java_import

class HDFSClient:
    CLASSPATH ="""
        {HADOOP_HOME}\\etc\\hadoop;{HADOOP_HOME}\\share\\hadoop\\common\\lib\\*;
        {HADOOP_HOME}\\share\\hadoop\\common\\*;
        {HADOOP_HOME}\\share\\hadoop\\hdfs;
        {HADOOP_HOME}\\share\\hadoop\\hdfs\\lib\\*;
        {HADOOP_HOME}\\share\\hadoop\\hdfs\\*;
        {HADOOP_HOME}\\share\\hadoop\\yarn;
        {HADOOP_HOME}\\share\\hadoop\\yarn\\lib\\*;
        {HADOOP_HOME}\\share\\hadoop\\yarn\\*;
        {HADOOP_HOME}\\share\\hadoop\\mapreduce\\lib\\*;
        {HADOOP_HOME}\\share\\hadoop\\mapreduce\\*;
        {JAVA_HOME}\\*
    """

    def __init__(self, **kwargs):
        HDFSClient.validate_environ('HADOOP_HOME')
        HDFSClient.validate_environ('JAVA_HOME')
        
        self.classpath = HDFSClient.CLASSPATH.format(
            HADOOP_HOME=os.environ['HADOOP_HOME'], JAVA_HOME = os.environ['JAVA_HOME']
        )
        
        self.jarpath = HDFSClient.get_jar_path()
        self.classpath = re.sub('\s+', '', self.classpath).replace('/', '\\') # removing spaces from class path
        self.classpath = re.sub(r'[\\]+', r'\\', self.classpath) # removing multiple sequencial slashes

        if not sys.platform.lower().startswith('win'): # updating classpath for non windows platforms
            self.classpath = self.classpath.replace('\\', '/').replace(";", ":")
            os.environ['TEMP'] = '/tmp'

        self.log_file_basepath = kwargs.get('log_file_basepath', os.path.join(
            os.environ.get('TEMP', '.'), 'pyhdfs_{}'.format(int(time.time() * 1000))))
        os.makedirs(self.log_file_basepath, exist_ok=True)
        
        self.update_hadoop_environ()
        self.launch_gateway()
        self.launch_hdfs_shell()

    @staticmethod
    def get_jar_path():
        if sys.platform.lower().startswith("win"):
            return ""
        search_dirs = ['/usr/share/py4j/', '/usr/local/share/py4j/']
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                jars = [jar for jar in os.listdir(search_dir) if re.search('py4j.*\.jar', jar)]
                if len(jars):
                    return os.path.join(search_dir, jars[0])
        return ""
 
    @staticmethod
    def validate_environ(varname):
        if varname not in os.environ:
            raise Exception("Required environment variable: {varname} not set!".format(varname=varname))

    def update_hadoop_environ(self):
        os.environ['HADOOP_CONF_DIR'] = os.path.join(os.environ['HADOOP_HOME'], r'etc\hadoop')
        os.environ['YARN_CONF_DIR'] = os.environ['HADOOP_CONF_DIR']
        os.environ['HADOOP_PREFIX'] = os.environ['HADOOP_HOME']
        os.environ['PATH'] = os.environ['PATH'] + ";" + os.path.join(os.environ['HADOOP_HOME'], r'bin')
        if not sys.platform.lower().startswith('win'):
            os.environ['PATH'] = os.environ['PATH'].replace(";", ":").replace("\\", '/')
            os.environ['HADOOP_CONF_DIR'] = os.environ['HADOOP_CONF_DIR'].replace(";", ":").replace("\\", '/')
            os.environ['YARN_CONF_DIR'] = os.environ['YARN_CONF_DIR'].replace(";", ":").replace("\\", '/')

    def update_log_files(self):
        self.out_file = os.path.join(self.log_file_basepath, 'out.log')
        self.err_file = os.path.join(self.log_file_basepath, 'err.log')
        self.out = open(self.out_file, 'w')
        self.err = open(self.err_file, 'w')

    def launch_gateway(self):

        self.update_log_files()
        port, proc = launch_gateway(
            classpath=self.classpath,
            redirect_stderr=self.err,
            redirect_stdout=self.out,
            die_on_exit=True,
            jarpath=self.jarpath,
            return_proc=True
        )
        self.java_pid = proc.pid
        
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=port),
            callback_server_parameters=CallbackServerParameters(port=0)
        )

        python_port = self.gateway.get_callback_server().get_listening_port()

        self.gateway.java_gateway_server.resetCallbackClient(
            self.gateway.java_gateway_server.getCallbackClient().getAddress(),
            python_port
        )

    def launch_hdfs_shell(self):
        java_import(self.gateway.jvm, 'org.apache.hadoop.fs.FsShell')
        java_import(self.gateway.jvm, 'org.apache.hadoop.conf.Configuration')
        self.fsshell = self.gateway.jvm.FsShell()
        conf = self.gateway.jvm.Configuration()
        conf.setQuietMode(False)
        self.fsshell.setConf(conf)

    def get_java_array(self, py_list):
        java_list = self.gateway.new_array(self.gateway.jvm.java.lang.String,len(py_list))
        for idx in range(len(py_list)):
            java_list[idx] = py_list[idx]
        return java_list

    def run(self, cmd):

        self.err.seek(0)
        self.err.truncate()

        print_stream = self.gateway.jvm.java.io.PrintStream(self.out_file)
        self.gateway.jvm.System.setOut(print_stream)
        ret = self.fsshell.run(self.get_java_array(cmd))
        print_stream.close()

        with open(self.out_file) as f:
            out = f.read()
        with open(self.err_file) as f:
            err = f.read()
        return ret, out, err

    def stop(self):
        self.gateway.shutdown()
        self.gateway.shutdown_callback_server()
        
        # wait for child process to exit
        os.kill(self.java_pid, 9)
        while psutil.pid_exists(self.java_pid):
            print("waiting for java process to terminate...")
            time.sleep(1)
        self.err.close()
        self.out.close()

        print("removing temp directory...",self.log_file_basepath)
        shutil.rmtree(self.log_file_basepath)

# set HADOOP_HOME and JAVA_HOME (C:\PROGRA~1 notation) in windows
if __name__=='__main__':
    hdfs_client = HDFSClient()
    print(hdfs_client.run(['-ls', '/']))
    hdfs_client.stop()