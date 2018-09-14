import json

try:
    import requests
except ImportError:
    raise ImportError("Missing dependency: python-requests")

"""
Error Classes
"""


class UnauthorizedError(Exception):
    pass


class RPCError(Exception):
    pass


class RPCConnection(Exception):
    pass


class HTTPRPC(object):
    def __init__(self, uri="", username="", password=""):
        if not uri:
            uri = "https://bitshares.openledger.info/ws"
        uri = uri.replace("wss://", "https://")
        self.uri = uri
        self.username = ""
        self.password = ""
        self.headers = {'content-type': 'application/json'}

    def rpcexec(self, payload):
        try:
            response = requests.post(
                self.uri,
                data=json.dumps(payload),
                headers=self.headers,
                auth=(self.username, self.password))
            if response.status_code == 401:
                raise UnauthorizedError
            ret = json.loads(response.text)
            if 'error' in ret:
                if 'detail' in ret['error']:
                    raise RPCError("call %s, error %s" % (
                        ret['error']['detail'], json.dumps(payload)))
                else:
                    raise RPCError("call %s, error %s" % (
                        ret['error']['message'], json.dumps(payload)))
        except requests.exceptions.RequestException:
            raise RPCConnection("Error connecting. Check hostname and port!")
        except UnauthorizedError:
            raise UnauthorizedError("Invalid login credentials!")
        except ValueError:
            raise ValueError("Client returned invalid format. Expected JSON!")
        except RPCError as err:
            raise err
        return ret["result"]

    """
    Meta:Map all methods to RPC calls and pass through the arguments and result
    """
    def __getattr__(self, name):
        def method(*args):
            query = {
                "method": "call",
                "params": [0, name, args],
                "jsonrpc": "2.0",
                "id": 0
            }
            r = self.rpcexec(query)
            return r
        return method

if __name__ == '__main__':
    import sys
    from pprint import pprint
    uri = ""
    if len(sys.argv) >= 2:
        uri = sys.argv[1]

    rpc = HTTPRPC(uri)
    pprint(rpc.get_dynamic_global_properties())