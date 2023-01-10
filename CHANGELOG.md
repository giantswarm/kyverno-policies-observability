# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Push to `cloud-director` app collection.
- Remove deprecated `validate` step from CI.

## [0.2.2] - 2022-11-29

- push to GCP collection

## [0.2.1] - 2022-11-21

### Fixed

- Relabel namespace only if it is not exported by the app.
- push to CAPA collection

## [0.2.0] - 2022-08-09

### Changed

- upgrade Kyverno 1.5.1 to 1.6
- upgrade Giantswarm CRDs v3.32.0 to v3.39.0

### Fixed

- README: instructions to run local tests
- podMonitor and serviceMoniter relabeling are added to existing config, rather than replacing it. Warning: that means their behavior could change!

## [0.1.3] - 2022-08-05

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

[Unreleased]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/kyverno-policies-observability/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/giantswarm/kyverno-policies-observability/releases/tag/v0.0.1
