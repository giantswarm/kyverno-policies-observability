import sys
sys.path.append('../../../tests')

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import release
from ensure import cluster
from ensure import machinedeployment
from ensure import kubeadmconfig
from ensure import kubeadmconfig_controlplane
from ensure import kubeadmconfig_with_labels
from ensure import kubeadmconfig_with_role_labels
from ensure import kubeadmconfig_with_kubelet_args
from ensure import kubeadm_control_plane
from ensure import kubeadmconfig_controlplane
from ensure import kubeadmconfig_with_files
from ensure import kubeadmconfig_with_audit_file
from ensure import podmonitor
from ensure import silence
from ensure import silence_with_matchers
from ensure import servicemonitor

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_kubeadmconfig_policy_controlplane(kubeadmconfig_controlplane) -> None:
    """
    test_kubeadmconfig_policy_controlplane tests defaulting of a KubeadmConfig for a control plane where all required values are empty strings.

    :param kubeadmconfig_controlplane: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig_controlplane['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig_controlplane['metadata']['labels']['cluster.x-k8s.io/control-plane'] == ""

@pytest.mark.smoke
def test_kubeadmconfig_auditpolicy(kubeadmconfig_with_files) -> None:
    """
    test_kubeadmconfig_auditpolicy tests defaulting of a kubeadmconfig with audit policy details

    :param kubeadmconfig_with_files: KubeadmConfig CR which includes some existing files
    """
    found = False
    for file in kubeadmconfig_with_files['spec']['files']:
        if file['path'] == "/etc/kubernetes/policies/audit-policy.yaml":
            found = True

    assert found == True

@pytest.mark.smoke
def test_kubeadmconfig_auditpolicy(kubeadmconfig_with_audit_file) -> None:
    """
    test_kubeadmconfig_auditpolicy tests defaulting of a kubeadmconfig with audit policy details

    :param kubeadmconfig_with_audit_file: KubeadmConfig CR which includes an existing audit file
    """
    assert len(kubeadmconfig_with_audit_file['spec']['files']) == 1


@pytest.mark.smoke
def test_silence_heartbeat_policy(silence) -> None:
    """
    test_silence_heartbeat_policy tests defaulting of an empty Silence to check for the negative Heartbeat matcher.
    :param silence: Any Silence CR.
    """
    matchers = silence['spec']['matchers']

    for matcher in matchers:
        if matcher['name'] == "alertname":
            assert (matcher['value'] == "Heartbeat" and not matcher['isRegex'] and not matcher['isEqual'])
            return

    pytest.fail("Heartbeat matcher is missing")

@pytest.mark.smoke
def test_silence_heartbeat_policy_with_existing_matchers(silence_with_matchers) -> None:
    """
    test_silence_heartbeat_policy tests defaulting of a Silence container a matcher to check for the negative Heartbeat matcher.
    :param silence_with_matchers: Any Silence CR container a matcher.
    """
    matchers = silence_with_matchers['spec']['matchers']

    assert (matchers[0]['value'] == "test" and matchers[0]['name'] == "test" and not matchers[0]['isRegex'] and not matchers[0]['isEqual'])
    assert (matchers[1]['value'] == "Heartbeat" and matchers[1]['name'] == "alertname" and not matchers[1]['isRegex'] and not matchers[1]['isEqual'])


@pytest.mark.smoke
def test_pod_monitor_labelling_schema_policy(podmonitor) -> None:
    """
    test_service_monitor_labelling_schema_policy tests defaulting of an empty Service monitor to check that the labelling schema is configured.
    :param podmonitor: Any PodMonitor CR.
    """
    endpoints = podmonitor['spec']['podMetricsEndpoints']
    for endpoint in endpoints:
        relabelings = endpoint['relabelings']
        assert relabelings[0]['replacement'] == '' and relabelings[0]['targetLabel'] == 'cluster_id'                                                       \
          and relabelings[1]['replacement'] == 'management_cluster' and relabelings[1]['targetLabel'] == 'cluster_type'                                    \
          and relabelings[2]['replacement'] == 'highest' and relabelings[2]['targetLabel'] == 'service_priority'                                           \
          and relabelings[3]['replacement'] == '' and relabelings[3]['targetLabel'] == 'provider'                                                          \
          and relabelings[4]['replacement'] == '' and relabelings[4]['targetLabel'] == 'installation'                                                      \
          and relabelings[5]['sourceLabels'] == ['__meta_kubernetes_namespace'] and relabelings[5]['targetLabel'] == 'namespace'                           \
          and relabelings[6]['sourceLabels'] == ['__meta_kubernetes_pod_label_app_kubernetes_io_name'] and relabelings[6]['targetLabel'] == 'app'          \
          and relabelings[7]['sourceLabels'] == ['__meta_kubernetes_pod_name'] and relabelings[7]['targetLabel'] == 'pod'                                  \
          and relabelings[8]['sourceLabels'] == ['__meta_kubernetes_pod_container_name'] and relabelings[8]['targetLabel'] == 'container'                  \
          and relabelings[9]['sourceLabels'] == ['__meta_kubernetes_pod_node_name'] and relabelings[9]['targetLabel'] == 'node'                            \
          and relabelings[10]['sourceLabels'] == ['__meta_kubernetes_node_label_role'] and relabelings[10]['targetLabel'] == 'role'                          \
          and relabelings[11]['replacement'] == '' and relabelings[11]['targetLabel'] == 'customer'                                                          \
          and relabelings[12]['replacement'] == 'default' and relabelings[12]['targetLabel'] == 'organization'                                             \
          and relabelings[13]['sourceLabels'] == ['organization'] and relabelings[13]['regex'] == 'org-(.*)' and relabelings[13]['replacement'] == '${1}' and relabelings[13]['targetLabel'] == 'organization' \
        , 'Invalid relabelings {} '.format(relabelings)

@pytest.mark.smoke
def test_service_monitor_labelling_schema_policy(servicemonitor) -> None:
    """
    test_service_monitor_labelling_schema_policy tests defaulting of an empty Service monitor to check that the labelling schema is configured.
    :param servicemonitor: Any ServiceMonitor CR.
    """
    endpoints = servicemonitor['spec']['endpoints']
    for endpoint in endpoints:
        relabelings = endpoint['relabelings']
        assert relabelings[0]['replacement'] == '' and relabelings[0]['targetLabel'] == 'cluster_id'                                                       \
          and relabelings[1]['replacement'] == 'management_cluster' and relabelings[1]['targetLabel'] == 'cluster_type'                                    \
          and relabelings[2]['replacement'] == 'highest' and relabelings[2]['targetLabel'] == 'service_priority'                                           \
          and relabelings[3]['replacement'] == '' and relabelings[3]['targetLabel'] == 'provider'                                                          \
          and relabelings[4]['replacement'] == '' and relabelings[4]['targetLabel'] == 'installation'                                                      \
          and relabelings[5]['sourceLabels'] == ['__meta_kubernetes_namespace'] and relabelings[5]['targetLabel'] == 'namespace'                           \
          and relabelings[6]['sourceLabels'] == ['__meta_kubernetes_pod_label_app_kubernetes_io_name'] and relabelings[6]['targetLabel'] == 'app'          \
          and relabelings[7]['sourceLabels'] == ['__meta_kubernetes_pod_name'] and relabelings[7]['targetLabel'] == 'pod'                                  \
          and relabelings[8]['sourceLabels'] == ['__meta_kubernetes_pod_container_name'] and relabelings[8]['targetLabel'] == 'container'                  \
          and relabelings[9]['sourceLabels'] == ['__meta_kubernetes_pod_node_name'] and relabelings[9]['targetLabel'] == 'node'                            \
          and relabelings[10]['sourceLabels'] == ['__meta_kubernetes_node_label_role'] and relabelings[10]['targetLabel'] == 'role'                          \
          and relabelings[11]['replacement'] == '' and relabelings[11]['targetLabel'] == 'customer'                                                          \
          and relabelings[12]['replacement'] == 'default' and relabelings[12]['targetLabel'] == 'organization'                                             \
          and relabelings[13]['sourceLabels'] == ['organization'] and relabelings[13]['regex'] == 'org-(.*)' and relabelings[13]['replacement'] == '${1}' and relabelings[13]['targetLabel'] == 'organization' \
        , 'Invalid relabelings {}'.format(relabelings)
