#!env bash
set -e

# need this variable to run the tests outside GOPATH
export REPO_ROOT=$(pwd)

if [[ ${CLUSTER} == "gke" ]]; then
  # Overlay CNI Parameters for GCP : https://github.com/tetratelabs/getistio/issues/76
  pip install pyyaml --user && ./tetrateci/gen_iop.py
  CLUSTERFLAGS="-istio.test.kube.helm.iopFile $(pwd)/tetrateci/iop-gke-integration.yml"
  git apply tetrateci/chiron-gke.patch
fi

if [[ ${CLUSTER} == "eks" ]]; then
  git apply tetrateci/eks-ingress.1.8.patch
fi

if [[ ${CLUSTER} == "aks" ]]; then
  # Just increasing the timeout though the test is disabled for now
  git apply tetrateci/aks-pilot.1.8.patch
fi

# go test -count=1 -tags=integ ./tests/integration/helm/...  -p 1 -test.v

# go test -count=1 -tags=integ ./tests/integration/operator/...   -p 1  -test.v
# # TestVmOSPost fails in gke
# go test -count=1 -tags=integ -timeout 30m ./tests/integration/pilot/ -run='TestAddToAndRemoveFromMesh|TestAllNamespaces|TestAuthZCheck|TestDescribe|TestDirectoryWithoutRecursion|TestDirectoryWithRecursion|TestEmptyCluster|TestEnsureNoMissingCRDs|TestErrorLine|TestFileAndKubeCombined|TestFileOnly|TestGateway|TestIngress|TestInvalidFileError|TestJsonInputFile|TestJsonOutput|TestKubeOnly|TestLocality|TestMain|TestMirroring|TestMirroringExternalService|TestProxyConfig|TestProxyStatus|TestTimeout|TestTraffic|TestValidation|TestVersion|TestWait|TestWebhook' -istio.test.skipVM true  -p 1 -test.v
# go test -count=1 -tags=integ ./tests/integration/pilot/analysis/...  -p 1 -test.v
# go test -count=1 -tags=integ ./tests/integration/pilot/revisions/...  -p 1 -test.v
# go test -count=1 -tags=integ ./tests/integration/pilot/endpointslice/. -istio.test.skipVM true  -p 1 -test.v
# go test -count=1 -tags=integ ./tests/integration/pilot/cni/... ${CLUSTERFLAGS} -p 1 -test.v

# go test -count=1 -tags=integ ./tests/integration/telemetry/requestclassification/...  -p 1 -test.v
# there is some problem with the prometheus
# go test -count=1 -tags=integ -timeout 30m  ./tests/integration/telemetry/outboundtrafficpolicy/...  -p 1 -test.v
go test -count=1 -tags=integ -timeout 30m ./tests/integration/telemetry/policy/. -test.v
# TestIstioCtlMetrics fails everywhere
go test -count=1 -tags=integ -timeout 30m ./tests/integration/telemetry/stats/... -p 1 -test.v -run "TestDashboard|TestSetup|TestStatsFilter|TestStatsTCPFilter|TestTcpMetric|TestWasmStatsFilter|TestWASMTcpMetric"
go test -count=1 -tags=integ -timeout 30m ./tests/integration/telemetry/tracing/... -p 1 -test.v

go test -count=1 -tags=integ -timeout 30m ./tests/integration/security/.  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/ca_custom_root/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/ecc_signature_algorithm/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/chiron/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/filebased_tls_origination/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/mtls_first_party_jwt/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/mtlsk8sca/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/sds_egress/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/sds_tls_origination/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/webhook/...  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/sds_ingress/.  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/sds_ingress_gateway/.  -p 1 -test.v
go test -count=1 -tags=integ ./tests/integration/security/sds_ingress_k8sca/.  -p 1 -test.v
