# kyverno-policies-observability

This repository contains kyverno policies which Giant Swarm uses for supporting monitoring and observability when working with Giant Swarm clusters.

## Repository structure

We implement an app according to the [general Giant Swarm app platform](https://docs.giantswarm.io/app-platform/) which relies on Helm for application management.

The `policies` folder contains the policies which are then escaped to be compliant with helm specific syntax.
We use `[[` and  `]]` delimeters to handle cases where variables should be managed by helm.

The `hack` folder contains scripts which are used during local development and in CI.
These scripts enable us to easily set up a local testing environment.

## Development

There are only very few prerequisites for local testing:
1. `make` has to be installed
1. `kubectl` has to be installed
1. `kind` has to be installed
1. `clusterctl` has to be installed (you may need an older version, like 1.3.2)
1. [dabs.sh](https://raw.githubusercontent.com/giantswarm/app-build-suite/v1.1.4/dabs.sh) has to be accessible.
1. [dats.sh](https://raw.githubusercontent.com/giantswarm/app-test-suite/v0.2.9/dats.sh) has to be accessible.

Tests are implemented with [pytest](https://docs.pytest.org) with plugin [pytest-helm-charts](https://github.com/giantswarm/pytest-helm-charts).

Executing the integration tests can be done with this simple set of commands:
```bash
make kind-create kind-get-kubeconfig install-kyverno # Creates the kind cluster and installs all dependencies.
./dabs.sh --generate-metadata -c ./helm/kyverno-policies-observability # Builds helm chart archive to be tested.
cp build/kyverno-policies-observability-*.tgz kyverno-policies-observability.tgz
./dats.sh --chart-file kyverno-policies-observability.tgz --app-tests-pytest-tests-dir helm/kyverno-policies-observability/tests/ats # Executes the tests
```

To only generate the policies in the `helm` folder structure:
```bash
make generate
```

### Adding tests

This repository uses the [app-build-suite](https://github.com/giantswarm/app-build-suite/) and the related testing setup.
We have tried to make the test setup as simple as possible but some python knowledge is required.

The tests use [python fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) extensively to set up any resources we need in our tests.

All fixtures can be found in [ensure.py](https://github.com/giantswarm/kyverno-policies-observability/blob/main/helm/tests/ensure.py).
Each fixtures should be structured in a similar way. Let's follow an example for `AWSCluster`:
```python
@pytest.fixture
def awscluster(kubernetes_cluster):
    # Yaml of whatever resource you want to create.
    # The cluster_name variable is defined globally in ensure.py - so we always reuse the same names.
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
        kind: AWSCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
        spec:
          region: ""
          sshKeyName: ""
    """)

    # Creating the resource for our test.
    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    # Get the resource back from Kubernetes after it has been applied / defaulted.
    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    # yield returns the object to our test case.
    yield awscluster

    # Do cleanup after our testcase has ended.
    kubernetes_cluster.kubectl(f"delete awscluster {cluster_name}", output=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")
```

The testcases can now look very simple as we only need to assert that the resources were created as we expected.
Here is an example for a AWSCluster policy:
```python
# We have to mark the test as smoke for app-build-suite.
@pytest.mark.smoke
# We request 3 resources from fixtures: a Release CR, a Cluster CR and an AWSCluster CR.
# The input parameters are named the same as the fixture functions to make it work.
def test_aws_cluster_policy(release, cluster, awscluster) -> None:
    """
    test_aws_cluster_policy tests defaulting of an AWSCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster: AWSCluster CR with empty strings which matches the Cluster CR.
    """
    # At this point the release CR, cluster CR and awscluster CR have all been created in our KIND setup.
    # We now only need to assert that the awscluster CR looks like we expect it to!
    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"
    # We don't need to clean up anything as the fixture does that for us already!
```
To make this example work in a new file we need to also remember to import our fixtures correctly:
```python
# Importing the path to the ensure.py file.
import sys
sys.path.append('../../../tests')
# Import the fixtures we need for our test cases!
from ensure import release
from ensure import cluster
from ensure import awscluster
```
And then we should be good to go!

The output of our testcase then also shows the different setup and teardown stages in the logs:
```
test_aws_default.py::test_aws_cluster_policy
------------------------------------- live log setup ----------------------------------------------------
INFO     ensure:ensure.py:55 Release v20.0.0 applied
INFO     ensure:ensure.py:92 Cluster test-cluster applied
INFO     ensure:ensure.py:193 AWSCluster test-cluster applied
PASSED                                                                                              [ 20%]
------------------------------------ live log teardown ---------------------------------------------------
INFO     ensure:ensure.py:203 AWSCluster test-cluster deleted
INFO     ensure:ensure.py:102 Cluster test-cluster deleted
```

### Tilt
You can use Tilt for fast feedback loops.

First create the local `kind` cluster
```shell
make kind-create
```

Then you just need to start `tilt`
```shell
make tilt-up
```
