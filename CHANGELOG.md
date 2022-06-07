# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2022-06-07

### Added

- Add `instance` label based on `app.kubernetes.io/instance` to pod and service monitorsg

## [0.1.1] - 2022-06-02

### Added

- Add `app` and `service-priority labels `ServiceMonitor` and `PodMonitor`

## [0.1.0] - 2022-05-27

### Added

- Add `ServiceMonitor` and `PodMonitor` default relabelling.

## [0.0.1] - 2022-03-31

### Added

- Initial policies moved from [`kyverno-policies`](https://github.com/giantswarm/kyverno-policies).
- Push to AWS, Azure, KVM, and OpenStack collections.

[Unreleased]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/giantswarm/kyverno-policies-observability/releases/tag/v0.0.1
