# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [2.9.0](https://github.com/seamapi/python/compare/v2.8.0...v2.9.0) (2023-03-17)


### Features

* Add selected_provider to ConnectWebview ([#81](https://github.com/seamapi/python/issues/81)) ([98a2474](https://github.com/seamapi/python/commit/98a24745b7b35040b4dc870ce45d91c8984cfdc0))

## [2.8.0](https://github.com/seamapi/python/compare/v2.7.0...v2.8.0) (2023-03-09)


### Features

* Add custom_metadata ([#75](https://github.com/seamapi/python/issues/75)) ([01be89c](https://github.com/seamapi/python/commit/01be89cf854fa1d244f448f1ab41113c166f6340))


### Bug Fixes

* parity with js changes ([59051b4](https://github.com/seamapi/python/commit/59051b40b9b43a87ebaa23d898ea1f2c4d417811))

## [2.7.0](https://github.com/seamapi/python/compare/v2.6.0...v2.7.0) (2023-02-28)


### Features

* send status to connect on workflow trigger ([8091b61](https://github.com/seamapi/python/commit/8091b61e6de3593b99aaf71083964be31ea3d9db))
* use different name to call always ([aae209d](https://github.com/seamapi/python/commit/aae209d212dbb08a613e2783dbbb3744f8443eed))

## [2.6.0](https://github.com/seamapi/python/compare/v2.5.0...v2.6.0) (2022-12-01)


### Features

* Add attempt_for_offline_device to access_codes.create ([#67](https://github.com/seamapi/python/issues/67)) ([279ba04](https://github.com/seamapi/python/commit/279ba04687107ebcc222b561eec4180551864286))

## [2.5.0](https://github.com/seamapi/python/compare/v2.4.0...v2.5.0) (2022-12-01)


### Features

* Do not wait for action action attempt on access_code.create ([7684c1f](https://github.com/seamapi/python/commit/7684c1fa10db8014cff04007fa9b041623d8a0fe))
* Return access code immediately from access_code.create ([b6ec63a](https://github.com/seamapi/python/commit/b6ec63a13158d8e575be35c4117bd6c5ac2d9d2d))

## [2.4.0](https://github.com/seamapi/python/compare/v2.3.0...v2.4.0) (2022-11-23)


### Features

* Create Access Codes against many devices with same code ([#60](https://github.com/seamapi/python/issues/60)) ([d0e856f](https://github.com/seamapi/python/commit/d0e856fb142c44abc3b32dd38fac0236283dd69e))

## [2.3.0](https://github.com/seamapi/python/compare/v2.2.0...v2.3.0) (2022-11-16)


### Features

* Merge pull request [#58](https://github.com/seamapi/python/issues/58) from seamapi/add-new-params-nov-14 ([acebae9](https://github.com/seamapi/python/commit/acebae9453aca7211da4d5d7d02f9c3bc80fc0a9))

## [2.2.0](https://github.com/seamapi/python/compare/v2.1.0...v2.2.0) (2022-10-13)


### Features

* Merge pull request [#57](https://github.com/seamapi/python/issues/57) from seamapi/feat-sentry ([20605d5](https://github.com/seamapi/python/commit/20605d5e23da3d5b772565a05c412ba0d2979bef))

## [2.1.0](https://github.com/seamapi/python/compare/v2.0.0...v2.1.0) (2022-10-12)


### Features

* Merge pull request [#56](https://github.com/seamapi/python/issues/56) from seamapi/feat-add-user-agent ([aa00ba2](https://github.com/seamapi/python/commit/aa00ba28ba72ab6f57c489a004e177a2e4016990))

## [2.0.0](https://github.com/seamapi/python/compare/v1.6.0...v2.0.0) (2022-10-12)


### ⚠ BREAKING CHANGES

* thrown exceptions will now be slightly different

### Features

* Merge pull request [#53](https://github.com/seamapi/python/issues/53) from seamapi/feat-centralized-requests ([000a164](https://github.com/seamapi/python/commit/000a164883e4517f38e186f697326a5fd503d432))

## [1.6.0](https://github.com/seamapi/python/compare/v1.5.0...v1.6.0) (2022-10-08)


### Features

* Merge pull request [#50](https://github.com/seamapi/python/issues/50) from seamapi/fill-connectwebview-props ([72fab41](https://github.com/seamapi/python/commit/72fab4136b7e72234240f60618b8eb80febdf02c)), closes [#26](https://github.com/seamapi/python/issues/26)

## [1.5.0](https://github.com/seamapi/python/compare/v1.4.0...v1.5.0) (2022-09-20)


### Features

* Merge pull request [#47](https://github.com/seamapi/python/issues/47) from seamapi/implement-events ([20e3ecb](https://github.com/seamapi/python/commit/20e3ecb5aa855312cd47f92f12f75ccbba20f58c)), closes [#33](https://github.com/seamapi/python/issues/33)

## [1.4.0](https://github.com/seamapi/python/compare/v1.3.0...v1.4.0) (2022-09-19)


### Features

* Merge pull request [#45](https://github.com/seamapi/python/issues/45) from seamapi/implement-devices-delete ([b4be008](https://github.com/seamapi/python/commit/b4be00814820a609f0e0c09dc3c3a67526f0d656)), closes [#36](https://github.com/seamapi/python/issues/36)
* Merge pull request [#46](https://github.com/seamapi/python/issues/46) from seamapi/get-connected-account-by-email ([e247042](https://github.com/seamapi/python/commit/e247042b05ea40a3cd78f1fba94a7a2be2d75cb0)), closes [#28](https://github.com/seamapi/python/issues/28)


### Bug Fixes

* Correct reference to Docker container ([077c005](https://github.com/seamapi/python/commit/077c005e904b5c268deea0cd53f989e0a43ed03a))
* Merge pull request [#44](https://github.com/seamapi/python/issues/44) from seamapi/fix-docker-reference ([e6d1365](https://github.com/seamapi/python/commit/e6d136516e8410f5220631b1e44bda7dcaa60716))

## [1.3.0](https://github.com/seamapi/python/compare/v1.2.0...v1.3.0) (2022-09-19)


### Features

* Merge pull request [#42](https://github.com/seamapi/python/issues/42) from seamapi/implement-delete-connected-account ([c4b55b5](https://github.com/seamapi/python/commit/c4b55b5722774f6dc700679ecd03fbc12028eda0)), closes [#27](https://github.com/seamapi/python/issues/27)

## [1.2.0](https://github.com/seamapi/python/compare/v1.1.5...v1.2.0) (2022-09-16)


### Features

* Merge pull request [#41](https://github.com/seamapi/python/issues/41) from seamapi/implement-device-update ([bd94e17](https://github.com/seamapi/python/commit/bd94e17bab7657d31e2f58049deb136b5d2a58a2)), closes [#29](https://github.com/seamapi/python/issues/29)

### [1.1.5](https://github.com/seamapi/python/compare/v1.1.4...v1.1.5) (2022-09-13)


### Bug Fixes

* Merge pull request [#38](https://github.com/seamapi/python/issues/38) from seamapi/fix-35 ([47d1597](https://github.com/seamapi/python/commit/47d15978187c3be769fee01f20cc7ab374443a3d)), closes [#35](https://github.com/seamapi/python/issues/35)

### [1.1.4](https://github.com/seamapi/python/compare/v1.1.3...v1.1.4) (2022-08-14)


### Bug Fixes

* Merge pull request [#24](https://github.com/seamapi/python/issues/24) from seamapi/device-errors ([daf4afc](https://github.com/seamapi/python/commit/daf4afcbd5576fdd48592f896c174eb7bd9f160f))

### [1.1.3](https://github.com/seamapi/python/compare/v1.1.2...v1.1.3) (2022-08-10)


### Bug Fixes

* Merge pull request [#23](https://github.com/seamapi/python/issues/23) from seamapi/connected-account-errors ([4afb4ea](https://github.com/seamapi/python/commit/4afb4ea81801cb042de592c279916ca72985429b))

### [1.1.2](https://github.com/seamapi/python/compare/v1.1.1...v1.1.2) (2022-08-05)


### Bug Fixes

* Merge pull request [#22](https://github.com/seamapi/python/issues/22) from seamapi/better-error-handling ([25d007a](https://github.com/seamapi/python/commit/25d007a4feaaab4e0fe94bcb528ec79dc8326915))

### [1.1.1](https://github.com/seamapi/python/compare/v1.1.0...v1.1.1) (2022-07-30)


### Bug Fixes

* Merge pull request [#21](https://github.com/seamapi/python/issues/21) from seamapi/access-code-status ([6422b90](https://github.com/seamapi/python/commit/6422b907f342e48e542f304915b8f3b3be747e68))

## [1.1.0](https://github.com/seamapi/python/compare/v1.0.1...v1.1.0) (2022-07-11)


### Features

* Merge pull request [#17](https://github.com/seamapi/python/issues/17) from seamapi/feat-update-access-codes ([777edbc](https://github.com/seamapi/python/commit/777edbcb1f26f16edc0bdedfc25564af64bac91b))

### [1.0.1](https://github.com/seamapi/python/compare/v1.0.0...v1.0.1) (2022-04-12)


### Bug Fixes

* add note about publishing to README ([c0023b5](https://github.com/seamapi/python/commit/c0023b5fd6da50f238a60ec7ab7262e82f91c96c))
* update workflow name ([45b23fe](https://github.com/seamapi/python/commit/45b23feff7c692cfc13c4e9d5734ebe0ea0d1482))

## 1.0.0 (2022-04-11)


### Features

* add release workflow ([5fd13f5](https://github.com/seamapi/python/commit/5fd13f5d3b941a3118345a98aa7deed54b10039a))
