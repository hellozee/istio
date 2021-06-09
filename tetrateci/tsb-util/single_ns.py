import os
from jinja2 import Template
import yaml
import base64
import copy
import argparse
from dataclasses import dataclass
from marshmallow_dataclass import class_schema

@dataclass
class config:
    namespace: str
    tenant: str
    count: int
    org: str
    cluster: str
    workspace: str

def read_config_yaml(filename):
    schema = class_schema(config)
    with open(filename) as file:
        yamlconfig = yaml.load(file, Loader=yaml.SafeLoader)
        return schema().load(yamlconfig)

script_path = os.path.dirname(os.path.realpath(__file__))

entries = {
    "name": "",
    "port": 8443,
    "hostname": "",
    "tls": {
        "mode": "SIMPLE",
        "secretName": "wilcard-credential",
    },
    "routing": {"rules": [{"route": {"host": ""}}]},
}

def save_file(fname, content):
    f = open(fname, "w")
    f.write(content)
    f.close()

def create_cert():
    os.mkdir("cert")
    os.system(
        "openssl req -x509 -sha256 -nodes -days 365 \
        -newkey rsa:4096 -subj '/C=US/ST=CA/O=Tetrateio/CN=tetrate.test.com' \
        -keyout cert/tetrate.test.com.key -out cert/tetrate.test.com.crt"
    )

    os.system(
        "openssl req -out cert/wildcard.tetrate.test.com.csr -newkey rsa:2048 \
        -nodes -keyout cert/wildcard.tetrate.test.com.key \
        -subj '/CN=*.tetrate.test.com/O=bookinfo organization'"
    )

    os.system(
        "openssl x509 -req -sha256 -days 365 -CA cert/tetrate.test.com.crt \
        -CAkey cert/tetrate.test.com.key \
        -set_serial 0 -in cert/wildcard.tetrate.test.com.csr \
        -out cert/wildcard.tetrate.test.com.crt"
    )

def create_secret(ns, fname):
    secret_name = "wilcard-credential"
    hostname = "wildcard.tetrate.test.com"
    keyfile = open("cert/" + hostname + ".key")
    certfile = open("cert/" + hostname + ".crt")

    t = open(script_path + "/templates/k8s-objects/secret.yaml")
    template = Template(t.read())
    r = template.render(
        name=secret_name,
        ns=ns,
        crtData=base64.b64encode(certfile.read().encode("utf-8")).decode("utf-8"),
        keyData=base64.b64encode(keyfile.read().encode("utf-8")).decode("utf-8"),
    )
    t.close()

    f = open(fname, "w")
    f.write(r)
    f.close()

    keyfile.close()
    certfile.close()

def create_trafficgen_secret(ns, fname):
    secret_name = ns + "-ca-cert"
    certfile = open("cert/tetrate.test.com.crt")

    t = open(script_path + "/templates/k8s-objects/trafficgen-secret.yaml")
    template = Template(t.read())
    r = template.render(
        name=secret_name,
        ns=ns,
        data=base64.b64encode(certfile.read().encode("utf-8")).decode("utf-8"),
    )
    t.close()

    f = open(fname, "w")
    f.write(r)
    f.close()

    certfile.close()
    return secret_name

def install_httpbin(index, namespace):
    instance_name = "httpbin" + index
    t = open(script_path + "/templates/k8s-objects/httpbin.yaml")
    template = Template(t.read())
    r = template.render(namespace=namespace, name=instance_name)
    t.close()
    save_file("generated/k8s-objects/httpbin" + index + ".yaml", r)

def main():
    parser = argparse.ArgumentParser(
        description="Spin up httpbin instances, all the flags are required and to be pre generated\n"
        + "Example:\n"
        + " pipenv run python single_ns.py --config httpbin-config.example.yaml\n"
        + "\nNote: All the arguments are pre generated and installed in the cluster.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--config", help="pass the config for the install", required=True
    )

    args = parser.parse_args()
    conf = read_config_yaml(args.config)

    namespace_yaml = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"labels": {"istio-injection": "enabled"}, "name": conf.namespace},
    }

    os.makedirs("generated/k8s-objects/", exist_ok=True)
    os.makedirs("generated/tsb-objects/", exist_ok=True)

    t = open(script_path + "/templates/tsb-objects/tenant.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=conf.org,
        tenantName=conf.tenant,
    )
    t.close()
    save_file("generated/tsb-objects/tenant.yaml", r)

    t = open(script_path + "/templates/tsb-objects/workspace-httpbin.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=conf.org,
        tenantName=conf.tenant,
        workspaceName=conf.workspace,
        ns=conf.namespace,
        clusterName=conf.cluster,
    )
    t.close()
    save_file("generated/tsb-objects/workspaces.yaml", r)

    # groups
    gateway_group = "httpbin-gateway-" + conf.namespace
    traffic_group = "httpbin-traffic-" + conf.namespace
    security_group = "httpbin-security-" + conf.namespace
    t = open(script_path + "/templates/tsb-objects/group-httpbin.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=conf.org,
        tenantName=conf.tenant,
        workspaceName=conf.workspace,
        gatewayGroupName=gateway_group,
        trafficGroupName=traffic_group,
        securityGroupName=security_group,
        ns=conf.namespace,
        clusterName=conf.cluster,
        mode="BRIDGED",
    )
    t.close()
    save_file("generated/tsb-objects/groups.yaml", r)

    # perm
    t = open(script_path + "/templates/tsb-objects/perm.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=conf.org,
        tenantName=conf.tenant,
        workspaceName=conf.workspace,
        trafficGroupName=traffic_group,
    )
    t.close()
    save_file("generated/tsb-objects/perm.yaml", r)

    t = open(script_path + "/templates/tsb-objects/bridged/security.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=conf.org,
        tenantName=conf.tenant,
        workspaceName=conf.workspace,
        securitySettingName="httpbin-security-setting-" + conf.namespace,
        securityGroupName=security_group,
    )
    t.close()
    save_file("generated/tsb-objects/security.yaml", r)

    f = open("generated/k8s-objects/01namespace.yaml", "w")
    yaml.dump(namespace_yaml, f)
    f.close()

    t = open(script_path + "/templates/k8s-objects/ingress.yaml")
    template = Template(t.read())
    r = template.render(ns=conf.namespace)
    t.close()
    save_file("generated/k8s-objects/ingress.yaml", r)

    create_cert()
    create_secret(conf.namespace, "generated/k8s-objects/secret.yaml")
    create_trafficgen_secret(
        conf.namespace, "generated/k8s-objects/trafficgen-secret.yaml"
    )

    gateway_yaml = {
        "apiVersion": "gateway.tsb.tetrate.io/v2",
        "kind": "IngressGateway",
        "Metadata": {
            "organization": conf.org,
            "name": "tsb-gateway",
            "group": gateway_group,
            "workspace": conf.workspace,
            "tenant": conf.tenant,
        },
        "spec": {
            "workloadSelector": {
                "namespace": conf.namespace,
                "labels": {"app": "tsb-gateway-" + conf.namespace},
            },
            "http": [],
        },
    }

    http_routes = []
    curl_calls = ""

    for i in range(conf.count):
        install_httpbin(str(i), conf.namespace)
        name = "httpbin" + str(i)
        entries["name"] = name
        hostname = name + ".tetrate.test.com"
        entries["hostname"] = hostname
        entries["routing"]["rules"][0]["route"]["host"] = (
            conf.namespace + "/" + name + "." + conf.namespace + ".svc.cluster.local"
        )
        http_routes.append(copy.deepcopy(entries))
        curl_calls += (
            "              curl https://"
            + hostname
            + " --connect-to "
            + hostname
            + ":443:$IP:$PORT --cacert /etc/bookinfo/bookinfo-ca.crt &>/dev/null\n"
        )
    gateway_yaml["spec"]["http"] = http_routes

    f = open("generated/tsb-objects/gateway.yaml", "w")
    yaml.dump(gateway_yaml, f)
    f.close()
    service_account = "httpbin-serviceaccount"
    t = open(script_path + "/templates/k8s-objects/role.yaml")
    template = Template(t.read())
    r = template.render(
        targetNS=conf.namespace, clientNS=conf.namespace, saName=service_account
    )
    t.close()
    save_file("generated/k8s-objects/role.yaml", r)

    t = open(script_path + "/templates/k8s-objects/traffic-gen-httpbin.yaml")
    template = Template(t.read())
    r = template.render(
        ns=conf.namespace,
        saName=service_account,
        secretName=conf.namespace + "-ca-cert",
        serviceName="tsb-gateway-" + conf.namespace,
        content=curl_calls,
    )
    t.close()
    save_file("generated/k8s-objects/traffic-gen.yaml", r)

if __name__ == "__main__":
    main()
