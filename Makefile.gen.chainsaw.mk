# DO NOT EDIT. Generated with:
#
#    devctl
#
#    https://github.com/giantswarm/devctl/blob/81cdf8c488f860faa1f635b5b9f73c50de363304/pkg/gen/input/makefile/internal/file/Makefile.gen.chainsaw.mk.template
#

SHELL:=/usr/bin/env bash

# Kind cluster name to use
KIND_CLUSTER_NAME ?= chainsaw-kyverno-cluster

# These values should be set by the outer environment / CircleCI environment config.
# repository: kindest/node
KUBERNETES_VERSION := v1.33.7
# repository: giantswarm/kyverno-crds
KYVERNO_VERSION := v1.16.0
KYVERNO_POLICIES_APP_NAME ?= kyverno-policies-observability

##@ Test

.PHONY: kind-create
kind-create: ## create kind cluster if needed
	kind create cluster --name="${KIND_CLUSTER_NAME}" --image="kindest/node:${KUBERNETES_VERSION}"

.PHONY: install-crds
install-crds:
	# Install Cluster API CRDs
	kubectl apply -f https://github.com/kubernetes-sigs/cluster-api/releases/download/v1.9.4/bootstrap-components.yaml
	# Install Giant Swarm monitoring CRDs (Silence CRD)
	kubectl apply -f https://raw.githubusercontent.com/giantswarm/monitoring/main/config/crd/bases/monitoring.giantswarm.io_silences.yaml
	# Wait for CRDs to be established
	kubectl wait --for=condition=Established crd kubeadmconfigs.bootstrap.cluster.x-k8s.io --timeout=60s || true
	kubectl wait --for=condition=Established crd silences.monitoring.giantswarm.io --timeout=60s || true

.PHONY: install-kyverno
install-kyverno: install-crds
	kubectl create -f https://github.com/kyverno/kyverno/releases/download/$(KYVERNO_VERSION)/install.yaml
	# Sometimes the next check executes faster than the deployment show up for the Kube API Server, so we need to wait for a second
	sleep 5
	kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kyverno -l app.kubernetes.io/component=admission-controller -n kyverno --timeout 300s

.PHONY: install-policies
install-policies:
	touch tests/chainsaw/values.yaml
	helm upgrade --install $(KYVERNO_POLICIES_APP_NAME) ./helm/$(KYVERNO_POLICIES_APP_NAME) --values ./tests/chainsaw/values.yaml

.PHONY: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONY: dabs
dabs: generate
	dabs.sh --generate-metadata --chart-dir helm/kyverno-policies-observability
