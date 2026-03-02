#!/usr/bin/env bash
# This script applies extra CRDs to the test cluster before running chainsaw tests.
# It is meant to be called from the CI pipeline or locally before running chainsaw.
#
# CRDs must be installed BEFORE the policies so that Kyverno can configure
# its admission webhook for those resource types at policy installation time.

set -euo pipefail

SILENCE_OPERATOR_CRD_BASE="https://raw.githubusercontent.com/giantswarm/silence-operator/main/config/crd/bases"

echo "Applying Silence CRDs from giantswarm/silence-operator..."
kubectl apply --server-side -f "${SILENCE_OPERATOR_CRD_BASE}/monitoring.giantswarm.io_silences.yaml"
kubectl apply --server-side -f "${SILENCE_OPERATOR_CRD_BASE}/observability.giantswarm.io_silences.yaml"
echo "Done."
