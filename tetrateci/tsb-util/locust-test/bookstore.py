from locust import HttpUser, SequentialTaskSet, task, constant
import requests
import os.path
import socket

# mock /etc/hosts
# lock it in multithreading or use multiprocessing if an endpoint is bound to multiple IPs frequently
etc_hosts = {}


# decorate python built-in resolver
def custom_resolver(builtin_resolver):
    def wrapper(*args, **kwargs):
        try:
            return etc_hosts[args[:2]]
        except KeyError:
            # fall back to builtin_resolver for endpoints not in etc_hosts
            return builtin_resolver(*args, **kwargs)

    return wrapper


# monkey patching
socket.getaddrinfo = custom_resolver(socket.getaddrinfo)


def _bind_ip(domain_name, port, ip):
    '''
    resolve (domain_name,port) to a given ip
    '''
    key = (domain_name, port)
    # (family, type, proto, canonname, sockaddr)
    value = (socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM, 6, '', (ip, port))
    etc_hosts[key] = [value]



service_port = ''
service_ip = ''
service_hostname = 't0w0demobkifnb0f.tetrate.test.com'
test_name = f't0w0demobkifnb0f-productpage'

def fetch_latest_service_details():
    '''
    Fetch the latest service details and update it in the global variables `service_port` and `service_ip`.
    '''
    # Reference the internal certificate authority (CA)
    CA_CERT='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    TOKEN_FILE='/var/run/secrets/kubernetes.io/serviceaccount/token'
    TOKEN = ''
    if(os.path.isfile(CA_CERT)):
        print('Cert file exists.')
    else:
        print('Cert done not file exists.')

    if(os.path.isfile(TOKEN_FILE)):
        print('Token file exists.')
    else:
        print('Token done not file exists.')

    with open(TOKEN_FILE, 'r') as f:
        TOKEN = f.read()

    global service_port
    global service_ip
    # 1. Fetch the service node port
    print('Getting service IP and PORT.')
    response = requests.get(url = f'https://kubernetes.default.svc/api/v1/namespaces/t0w0demobkifnb0f/services/tsb-gateway-t0w0demobkifnb0f', verify= CA_CERT, headers={'Authorization': f'Bearer {TOKEN}'})
    data = response.json()
    for port_details in data['spec']['ports']:
        if port_details['port'] == 443:
            service_port = port_details['nodePort']
    # 2. Fetch the node IP
    response = requests.get(url = f'https://kubernetes.default.svc/api/v1/nodes', verify= CA_CERT, headers={'Authorization': f'Bearer {TOKEN}'})
    data = response.json()
    for address_details in data['items'][0]['status']['addresses']:
        if address_details['type']=='InternalIP':
            service_ip = address_details['address']
    _bind_ip(service_hostname, service_port, service_ip)

fetch_latest_service_details()

class BookStore(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    global service_port
    global service_ip
    global service_hostname
    global test_name
    @task
    def enter_store(self):
        with self.client.get(f'https://{service_hostname}:{service_port}/productpage', catch_response=True, name=test_name, verify='/etc/bookinfo/bookinfo-ca.crt', headers={'host': service_hostname}) as response:
            if "The Comedy of Errors" in response.text:
                response.success()
            else:
                response.failure(f"Product page text check has failed. Status code - {response.status_code} Text - {response.text}")
                fetch_latest_service_details()
                response.raise_for_status()

class LoadTest(HttpUser):
    host = 'https://t0w0demobkifnb0f.tetrate.test.com'
    wait_time = constant(1)
    tasks = [BookStore]
