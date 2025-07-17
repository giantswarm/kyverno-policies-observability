#!/usr/bin/env bash

# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster \
    -f https://raw.githubusercontent.com/giantswarm/apiextensions/v6.6.0/helm/crds-common/templates/application.giantswarm.io_appcatalogentries.yaml \
    -f https://raw.githubusercontent.com/giantswarm/apiextensions/v6.6.0/helm/crds-common/templates/application.giantswarm.io_appcatalogs.yaml \
    -f https://raw.githubusercontent.com/giantswarm/apiextensions/v6.6.0/helm/crds-common/templates/application.giantswarm.io_apps.yaml \
    -f https://raw.githubusercontent.com/giantswarm/apiextensions/v6.6.0/helm/crds-common/templates/application.giantswarm.io_catalogs.yaml \
    -f https://raw.githubusercontent.com/giantswarm/apiextensions/v6.6.0/helm/crds-common/templates/application.giantswarm.io_charts.yaml \
    -f https://raw.githubusercontent.com/giantswarm/silence-operator/main/config/crd/bases/monitoring.giantswarm.io_silences.yaml \
    -f https://raw.githubusercontent.com/giantswarm/silence-operator/main/config/crd/bases/observability.giantswarm.io_silences.yaml \
    -f https://raw.githubusercontent.com/giantswarm/releases/sdk/v0.10.0/sdk/manifests/apiextensions.k8s.io_v1_customresourcedefinition_releases.release.giantswarm.io.yaml \
    -f https://raw.githubusercontent.com/giantswarm/organization-operator/v2.0.1/config/crd/bases/security.giantswarm.io_organizations.yaml

MOCK_CREDENTIALS=$(echo -n "something" | base64)

export AWS_B64ENCODED_CREDENTIALS="${MOCK_CREDENTIALS}"

export AZURE_SUBSCRIPTION_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_TENANT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_SECRET_B64="${MOCK_CREDENTIALS}"

export EXP_MACHINE_POOL="true"
clusterctl init --infrastructure=aws,azure
kubectl --context kind-kyverno-cluster wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-aws -A
kubectl --context kind-kyverno-cluster wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-azure -A
