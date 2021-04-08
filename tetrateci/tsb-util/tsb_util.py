import urllib.request
import os, sys, shutil, platform

tag = "1.9.2-tetrate-v0"

client_os = "linux"

if platform.system() == "Darwin":
    os = "osx"
elif platform.system() == "Windows":
    print("Try Mac OS or Linux.")
    sys.exit()

print("Arch is set to amd64 no other architectures are supported for now.")

arch = "amd64"
archive_type = ".tar.gz"

base_url = "https://bintray.com/api/ui/download/tetrate/getistio/istio"
download_url = base_url + "-" + tag + "-" + client_os + "-" + arch + archive_type

print("Fetching istio from " + download_url)
temp_path = "/tmp/istio"
urllib.request.urlretrieve(download_url, temp_path + archive_type)

print("Upacking archive : " + temp_path + archive_type)
shutil.unpack_archive(temp_path + archive_type, "/tmp")

folder_name = "istio-" + tag
command = "/tmp/" + folder_name + "/bin/istioctl install -y"
print("Installing istio with :" + command)
os.system("/tmp/" + folder_name + "/bin/istioctl install -y")

bookinfo_instances = 6

services = ["productpage", "ratings", "details", "reviews"]
base_cmd = "kubectl apply -f /tmp/" + folder_name + "/samples/bookinfo/platform/kube/bookinfo.yaml -n "
i = 0
while i < bookinfo_instances:

    if services[i%4] == "reviews":

        j = 1

        while i < bookinfo_instances and j <= 3:
            print("Installing Bookinfo")
            ver = str(j)

            ns = "bookinfo" + str(i)
            print("Create Namespace : " + ns)
            os.system("kubectl create ns " + ns)
            os.system("kubectl label namespace " + ns + " istio-injection=enabled")

            print("Installing reviews-v" + ver)
            os.system(base_cmd + ns + " -l account=reviews")
            os.system(base_cmd + ns + " -l app=reviews,version=v" + ver)
            os.system(base_cmd + ns + " -l service=reviews")
            
            j += 1
            i += 1

            print("Bookinfo installed\n")

        continue


    print("Installing Bookinfo")

    ns = "bookinfo" + str(i)
    print("Create Namespace : " + ns)
    os.system("kubectl create ns " + ns)
    os.system("kubectl label namespace " + ns + " istio-injection=enabled")

    print("Installing " + services[i%4])
    os.system(base_cmd + ns + " -l account=" + services[i%4])
    os.system(base_cmd + ns + " -l app=" + services[i%4])

    i += 1

    print("Bookinfo installed\n")
