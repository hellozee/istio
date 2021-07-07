## How to run the test
To run the test, first make sure that you are connected to your cluster via `kubectl`. Then apply the `configmay.yaml`, `master.yaml` and then apply the `worker.yaml`.

Once this is done and both master and worker are up and running you will have to port-forward the master on you local like this:

`kubectl port-forward deploy/master -n t0w0demobkifnb0f 8089:8089`

And open [http:localhost:8089](http:localhost:8089) and you should be able to see the locust UI. Now fill in the correct values for users and spawn rate and start the test. You can view the test results on the UI it self. Note that you will have to stop the test manually.

### Note: 
This test/scripts are still underdevelopment, all the scripts/yamls are not directly usable, one may need to update the urls and namespaces in all the 3 yamls files to make it work. The idea in the long run is to not use configmap instead we will bake the information in the docker file itself and use few env variables to tweak things.