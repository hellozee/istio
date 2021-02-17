#!env bash
set -e

git apply tetrateci/patches/common/disable-dashboard.1.9.patch
git apply tetrateci/patches/common/disable-ratelimiting.1.9.patch
git apply tetrateci/patches/common/disable-stackdriver.1.9.patch

if $(grep -q "1.17" <<< ${VERSION} ); then
  git apply tetrateci/patches/common/disable-endpointslice.1.9.patch
fi

if [[ ${CLUSTER} == "gke" ]]; then
  # Overlay CNI Parameters for GCP : https://github.com/tetratelabs/getistio/issues/76
  pip install pyyaml --user && ./tetrateci/gen_iop.py
  CLUSTERFLAGS="-istio.test.kube.helm.iopFile $(pwd)/tetrateci/iop-gke-integration.yml"
  git apply tetrateci/patches/gke/chiron-gke.patch
fi

if [[ ${CLUSTER} == "eks" ]]; then
  git apply tetrateci/patches/eks/eks-ingress.1.9.patch
fi

export TAG=1.9.0-test
export HUB=hellozee-docker-istio-testing.bintray.io

go test -p 1 -test.v -tags=integ $(go list -tags=integ ./tests/integration/... | grep -v /qualification | grep -v /examples) -timeout 30m --istio.test.select=-postsubmit,-flaky,-multicluster
