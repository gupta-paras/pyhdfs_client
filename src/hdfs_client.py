from py4j.java_gateway import JavaGateway, GatewayParameters

class HDFSClient:
    def __init__(self, **kwargs):
        port = kwargs.get('port', 25333)
        self.gateway = self.launch_gateway()
        self.shell = self.gateway.entry_point.GetWrapper()

    def launch_gateway(self):
        raise NotImplementedError

    def dfs_execute(self, args):
        jvm_array = self.gateway.new_array(self.gateway.jvm.java.lang.String, len(args))
        for idx, arg in enumerate(args):
            jvm_array[idx] = arg
        # capture stdout, stderr