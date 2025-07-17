import sys
sys.path.append('../../../tests')

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
from ensure import silence
from ensure import silence_with_matchers

import pytest

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

    # Check that we have exactly 2 matchers (alertname and all_pipelines)
    assert len(matchers) == 2
    
    # Find and validate the alertname matcher
    alertname_matcher = None
    all_pipelines_matcher = None
    
    for matcher in matchers:
        if matcher['name'] == "alertname":
            alertname_matcher = matcher
        elif matcher['name'] == "all_pipelines":
            all_pipelines_matcher = matcher
    
    # Assert alertname matcher exists and has correct values
    assert alertname_matcher is not None, "alertname matcher is missing"
    assert (alertname_matcher['value'] == "Heartbeat" and 
            not alertname_matcher['isRegex'] and 
            not alertname_matcher['isEqual'])
    
    # Assert all_pipelines matcher exists and has correct values
    assert all_pipelines_matcher is not None, "all_pipelines matcher is missing"
    assert (all_pipelines_matcher['value'] == "true" and 
            not all_pipelines_matcher['isRegex'] and 
            not all_pipelines_matcher['isEqual'])

@pytest.mark.smoke
def test_silence_heartbeat_policy_with_existing_matchers(silence_with_matchers) -> None:
    """
    test_silence_heartbeat_policy tests defaulting of a Silence container a matcher to check for the negative Heartbeat matcher.
    :param silence_with_matchers: Any Silence CR container a matcher.
    """
    matchers = silence_with_matchers['spec']['matchers']

    # Should have 3 matchers: original test matcher + alertname + all_pipelines
    assert len(matchers) == 3

    # Validate the original test matcher (should be first)
    assert (matchers[0]['value'] == "test" and 
            matchers[0]['name'] == "test" and 
            not matchers[0]['isRegex'] and 
            not matchers[0]['isEqual'])

    # Find and validate the added matchers
    alertname_matcher = None
    all_pipelines_matcher = None

    for matcher in matchers:  # Skip the first matcher (test matcher)
        if matcher['name'] == "alertname":
            alertname_matcher = matcher
        elif matcher['name'] == "all_pipelines":
            all_pipelines_matcher = matcher

    # Assert alertname matcher exists and has correct values
    assert alertname_matcher is not None, "alertname matcher is missing"
    assert (alertname_matcher['value'] == "Heartbeat" and 
            not alertname_matcher['isRegex'] and 
            not alertname_matcher['isEqual'])

    # Assert all_pipelines matcher exists and has correct values
    assert all_pipelines_matcher is not None, "all_pipelines matcher is missing"
    assert (all_pipelines_matcher['value'] == "true" and 
            not all_pipelines_matcher['isRegex'] and 
            not all_pipelines_matcher['isEqual'])
