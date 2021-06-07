import os
import sys
import argparse
import config
import certs
from jinja2 import Template

script_path = os.path.dirname(os.path.realpath(__file__))

def save_file(fname, content):
    f = open(fname, "w")
    f.write(content)
    f.close()

def generate_bookinfo_yaml(namespaces, key):
    svc_domain = ".svc.cluster.local"
    details_env = "details." + namespaces["reviews"] + svc_domain
    reviews_env = "reviews." + namespaces["reviews"] + svc_domain
    ratings_env = "ratings." + namespaces["ratings"] + svc_domain

    t = open(script_path + "/templates/k8s-objects/bookinfo.yaml")
    template = Template(t.read())
    r = template.render(
        reviewsns=namespaces["reviews"],
        ratingsns=namespaces["ratings"],
        productns=namespaces["product"],
        detailsHostName=details_env,
        reviewsHostName=reviews_env,
        ratingsHostName=ratings_env,
    )
    t.close()
    save_file("generated/k8s-objects/" + key + "/bookinfo.yaml", r)

def gen_common_tsb_objects(
    namespaces, key, conf, tenant_name, workspace_name, mode, org
):
    # workspace
    t = open(script_path + "/templates/tsb-objects/workspace.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        ns1=namespaces["reviews"],
        ns2=namespaces["ratings"],
        ns3=namespaces["product"],
        clusterName=conf.cluster_name,
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/workspaces.yaml", r)

    # groups
    gateway_group = "bookinfo-gateway-" + key
    traffic_group = "bookinfo-traffic-" + key
    security_group = "bookinfo-security-" + key
    t = open(script_path + "/templates/tsb-objects/group.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        gatewayGroupName=gateway_group,
        trafficGroupName=traffic_group,
        securityGroupName=security_group,
        productNs=namespaces["product"],
        reviewsNs=namespaces["reviews"],
        ratingsNs=namespaces["ratings"],
        clusterName=conf.cluster_name,
        mode=mode.upper(),
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/groups.yaml", r)

    # perm
    t = open(script_path + "/templates/tsb-objects/perm.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        trafficGroupName=traffic_group,
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/perm.yaml", r)

    return gateway_group, traffic_group, security_group

def gen_namespace_yamls(namespaces, key):
    t = open(script_path + "/templates/k8s-objects/namespaces.yaml")
    template = Template(t.read())
    r = template.render(
        reviewsns=namespaces["reviews"],
        ratingsns=namespaces["ratings"],
        productns=namespaces["product"],
    )
    t.close()
    save_file("generated/k8s-objects/" + key + "/01namespaces.yaml", r)

def gen_bridge_specific_objects(
    tenant_name,
    workspace_name,
    traffic_group,
    gateway_group,
    security_group,
    namespaces,
    key,
    password,
    org,
    provider,
    tctl_ver,
):
    os.mkdir("generated/tsb-objects/" + key + "/bridged")
    os.mkdir("generated/k8s-objects/" + key + "/bridged")

    # security
    t = open(script_path + "/templates/tsb-objects/bridged/security.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        securitySettingName="bookinfo-security-setting",  # need to change
        securityGroupName=security_group,
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/bridged/security.yaml", r)

    servicerouteFile = script_path + "/templates/tsb-objects/bridged/serviceroute.yaml"
    t = open(servicerouteFile)
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        groupName=traffic_group,
        hostFQDN="reviews." + namespaces["reviews"] + ".svc.cluster.local",
        serviceRouteName="bookinfo-serviceroute",  # need to change
        ns=namespaces["reviews"],
    )
    save_file("generated/tsb-objects/" + key + "/bridged/serviceroute.yaml", r)
    t.close()

    gatewayFile = script_path + "/templates/tsb-objects/bridged/gateway.yaml"
    t = open(gatewayFile)
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        gatewayName=namespaces["product"] + "-gateway",
        hostname=namespaces["product"] + ".tetrate.test.com",
        gwSecretName=namespaces["product"] + "-credential",
        gatewayGroupName=gateway_group,
        ns=namespaces["product"],
        hostFQDN="productpage." + namespaces["product"] + ".svc.cluster.local",
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/bridged/gateway.yaml", r)

    t = open(script_path + "/templates/k8s-objects/bridged/servicerouteeditor.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenant=tenant_name,
        workspaceName=workspace_name,
        trafficGroupName=traffic_group,
        hostFQDN="reviews." + namespaces["reviews"] + ".svc.cluster.local",
        serviceRouteName="bookinfo-serviceroute",  # need to change
        ns=namespaces["reviews"],
        password=password,
        servicerouteSAName=namespaces["reviews"] + "-editor",
        podName=namespaces["reviews"] + "-editorpod",
        provider=provider,
        tctlVersion=tctl_ver,
    )
    save_file("generated/tsb-k8s-objects/" + key + "/servicerouteeditor.yaml", r)
    t.close()

def gen_direct_specific_objects(
    tenant_name,
    workspace_name,
    traffic_group,
    gateway_group,
    namespaces,
    key,
    password,
    org,
    provider,
    tctl_ver,
):
    os.mkdir("generated/tsb-objects/" + key + "/direct")
    os.mkdir("generated/k8s-objects/" + key + "/direct")
    # reviews virtual service
    reviews_vs = script_path + "/templates/tsb-objects/direct/reviews-vs.yaml"
    t = open(reviews_vs)
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        trafficGroupName=traffic_group,
        hostFQDN="reviews." + namespaces["reviews"] + ".svc.cluster.local",
        serviceRouteName="bookinfo-reviews",  # need to change
        ns=namespaces["reviews"],
    )
    save_file("generated/tsb-objects/" + key + "/direct/reviews_vs.yaml", r)
    t.close()

    t = open(script_path + "/templates/k8s-objects/direct/servicerouteeditor.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenant=tenant_name,
        workspaceName=workspace_name,
        trafficGroupName=traffic_group,
        hostFQDN="reviews." + namespaces["reviews"] + ".svc.cluster.local",
        serviceRouteName="bookinfo-serviceroute",  # need to change
        ns=namespaces["reviews"],
        password=password,
        servicerouteSAName=namespaces["reviews"] + "-editor",
        podName=namespaces["reviews"] + "-editorpod",
        provider=provider,
        tctlVersion=tctl_ver,
    )
    save_file("generated/tsb-k8s-objects/" + key + "/servicerouteeditor.yaml", r)

    # destination rules
    t = open(script_path + "/templates/tsb-objects/direct/dr.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        trafficGroupName=traffic_group,
        hostFQDN="reviews." + namespaces["reviews"] + ".svc.cluster.local",
        destinationruleName="bookinfo-destinationrule",  # need to change
        ns=namespaces["reviews"],
    )
    save_file("generated/tsb-objects/" + key + "/direct/destinationrule.yaml", r)
    t.close()

    # virtual service for product page
    t = open(script_path + "/templates/tsb-objects/direct/vs.yaml")
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        gatewayGroupName=gateway_group,
        hostFQDN=namespaces["product"] + ".tetrate.test.com",
        virtualserviceName="bookinfo-virtualservice",  # need to change
        ns=namespaces["product"],
        gatewayName=namespaces["product"] + "-gateway",
        destinationFQDN="productpage." + namespaces["product"] + ".svc.cluster.local",
    )
    save_file("generated/tsb-objects/" + key + "/direct/virtualservice.yaml", r)
    t.close()

    # gateway
    gatewayFile = script_path + "/templates/tsb-objects/direct/gw.yaml"
    t = open(gatewayFile)
    template = Template(t.read())
    r = template.render(
        orgName=org,
        tenantName=tenant_name,
        workspaceName=workspace_name,
        gatewayName=namespaces["product"] + "-gateway",
        hostname=namespaces["product"] + ".tetrate.test.com",
        gwSecretName=namespaces["product"] + "-credential",
        gatewayGroupName=gateway_group,
        ns=namespaces["product"],
        hostFQDN=namespaces["product"] + ".tetrate.test.com",
    )
    t.close()
    save_file("generated/tsb-objects/" + key + "/direct/gateway.yaml", r)

def install_bookinfo(conf, password, org, count=0, provider="others", tctl_ver="1.2.0"):
    for replica in conf.replicas:
        i = 0

        modes_list = modes_list = ["bridged"] * replica.bridged + [
            "direct"
        ] * replica.direct

        while i < (replica.bridged + replica.direct):
            print("Installing Bookinfo")
            key = str(count)

            current_mode = modes_list[i]

            tenant_id = str(replica.tenant_id)
            tenant_name = "bookinfo-tenant-" + tenant_id

            mode = "d" if current_mode == "direct" else "b"
            workspace_name = "bookinfo-ws-" + mode + key
            os.makedirs("generated/k8s-objects/" + key, exist_ok=True)
            os.makedirs("generated/tsb-objects/" + key, exist_ok=True)
            os.makedirs("generated/tsb-k8s-objects/" + key, exist_ok=True)

            productns = "bookinfo-" + mode + key + "-t" + tenant_id + "-front"
            reviewsns = "bookinfo-" + mode + key + "-t" + tenant_id + "-mid"
            ratingsns = "bookinfo-" + mode + key + "-t" + tenant_id + "-back"

            namespaces = {
                "product": productns,
                "ratings": ratingsns,
                "reviews": reviewsns,
            }

            generate_bookinfo_yaml(namespaces, key)

            gateway_group, traffic_group, security_group = gen_common_tsb_objects(
                namespaces, key, conf, tenant_name, workspace_name, current_mode, org
            )

            gen_namespace_yamls(namespaces, key)

            if current_mode == "bridged":
                gen_bridge_specific_objects(
                    tenant_name,
                    workspace_name,
                    traffic_group,
                    gateway_group,
                    security_group,
                    namespaces,
                    key,
                    password,
                    org,
                    provider,
                    tctl_ver,
                )
            else:
                gen_direct_specific_objects(
                    tenant_name,
                    workspace_name,
                    traffic_group,
                    gateway_group,
                    namespaces,
                    key,
                    password,
                    org,
                    provider,
                    tctl_ver,
                )

            gen_k8s_objects(
                productns,
                key,
                "InternalIP" if conf.traffic_gen_ip == "internal" else "ExternalIP",
            )

            print("Bookinfo installed\n")
            i += 1
            count += 1
    return count

def gen_k8s_objects(productns, key, iptype):

    certs.create_private_key(productns)
    certs.create_cert(productns)
    certs.create_secret(productns, "generated/k8s-objects/" + key + "/secret.yaml")

    # ingress
    t = open(script_path + "/templates/k8s-objects/ingress.yaml")
    template = Template(t.read())
    r = template.render(
        ns=productns,
    )
    t.close()
    save_file("generated/k8s-objects/" + key + "/ingress.yaml", r)

    service_account = productns + "-trafficegen-sa"

    # trafficgen

    secret_name = certs.create_trafficgen_secret(
        productns, "generated/k8s-objects/" + key + "/" + productns + "-secret.yaml"
    )

    t = open(script_path + "/templates/k8s-objects/role.yaml")
    template = Template(t.read())
    r = template.render(targetNS=productns, clientNS=productns, saName=service_account)
    t.close()
    save_file("generated/k8s-objects/" + key + "/role.yaml", r)

    t = open(script_path + "/templates/k8s-objects/traffic-gen.yaml")
    template = Template(t.read())
    r = template.render(
        ns=productns,
        hostname=productns + ".tetrate.test.com",
        saName=service_account,
        secretName=secret_name,
        serviceName="tsb-gateway-" + productns,
        ipType=iptype,
    )
    t.close()
    save_file("generated/k8s-objects/" + key + "/traffic-gen.yaml", r)

def main():
    parser = argparse.ArgumentParser(description="Spin up bookinfo instances")

    parser.add_argument(
        "--config", help="the yaml configuration for the bookinfo instances"
    )
    parser.add_argument(
        "--password", help="password for the admin user in the tsb instance"
    )
    args = parser.parse_args()

    if args.config is None:
        print("Pass in the config file with the `--config` flag")
        sys.exit(1)

    configs = config.read_config_yaml(args.config)

    if configs.provider not in ["aws", "others"]:
        print(
            "Possible values for provider is `aws` and `others` not", configs.provider
        )
        sys.exit(1)

    password = "admin"
    if args.password is not None:
        password = args.password

    certs.create_root_cert()

    os.mkdir("generated")

    tenant_count = 0

    for conf in configs.app:
        for replica in conf.replicas:
            tenant_count = max(tenant_count, replica.tenant_id)
    tenant_count += 1

    for tenant in range(tenant_count):
        tenant_name = "bookinfo-tenant-" + str(tenant)
        t = open(script_path + "/templates/tsb-objects/tenant.yaml")
        template = Template(t.read())
        r = template.render(
            orgName=configs.org,
            tenantName=tenant_name,
        )
        t.close()
        save_file("generated/tenant" + str(tenant) + ".yaml", r)
    count = 0
    for conf in configs.app:
        count = install_bookinfo(
            conf, password, configs.org, count, configs.provider, configs.tctl_version
        )

if __name__ == "__main__":
    main()
