# CHANGELOG


## v0.15.1 (2025-11-04)

### Bug Fixes

- Resolve dependency conflicts by removing incompatible version pins
  ([`c84fc5b`](https://github.com/milsman2/disc-golf-api/commit/c84fc5bba760a3dacbd12738a1a5c698af2ed9e7))

- Upgrade dependencies with uv sync --upgrade
  ([`3d016ac`](https://github.com/milsman2/disc-golf-api/commit/3d016acda4f8b6b87289ac940b61c7163c1ba6b1))

### Chores

- **deps**: Bump actions/checkout from 4 to 5
  ([`841dfb8`](https://github.com/milsman2/disc-golf-api/commit/841dfb80a1098fc0ec93d08132d1c70249ca3082))

Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 5. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v4...v5)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '5'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump actions/setup-python from 5 to 6
  ([`8547dff`](https://github.com/milsman2/disc-golf-api/commit/8547dffd10bec6ef2915960d93487559667ebce6))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump aquasecurity/trivy-action from 0.28.0 to 0.33.1
  ([`8383fd7`](https://github.com/milsman2/disc-golf-api/commit/8383fd7adbb8b7f60af78ef07550868367487168))

Bumps [aquasecurity/trivy-action](https://github.com/aquasecurity/trivy-action) from 0.28.0 to
  0.33.1. - [Release notes](https://github.com/aquasecurity/trivy-action/releases) -
  [Commits](https://github.com/aquasecurity/trivy-action/compare/0.28.0...0.33.1)

--- updated-dependencies: - dependency-name: aquasecurity/trivy-action dependency-version: 0.33.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump pytest in the development-dependencies group
  ([`6e74c47`](https://github.com/milsman2/disc-golf-api/commit/6e74c479af6b2adc34dcb773b7eb984648a853bf))

Bumps the development-dependencies group with 1 update:
  [pytest](https://github.com/pytest-dev/pytest).

Updates `pytest` from 8.4.1 to 8.4.2 - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.4.1...8.4.2)

--- updated-dependencies: - dependency-name: pytest dependency-version: 8.4.2

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: development-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([`87964f3`](https://github.com/milsman2/disc-golf-api/commit/87964f3df514eec0e623270522dc39ea7bcc93ab))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 9.21.0 to 10.4.1. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v9.21.0...v10.4.1)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: 10.4.1

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Refactoring

- Rename SessionDep to session_dep for consistency across modules
  ([`8008d9d`](https://github.com/milsman2/disc-golf-api/commit/8008d9dcf589daf2900473795e68c11ac85d0b17))


## v0.15.0 (2025-11-04)

### Chores

- **deps**: Bump the production-dependencies group with 64 updates
  ([`fa2cdb9`](https://github.com/milsman2/disc-golf-api/commit/fa2cdb95666f065603391ccceda10be2201c4551))

--- updated-dependencies: - dependency-name: aiohttp dependency-version: 3.13.2

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: production-dependencies

- dependency-name: alembic dependency-version: 1.17.1

- dependency-name: anyio dependency-version: 4.11.0

- dependency-name: astroid dependency-version: 4.0.1

update-type: version-update:semver-major

- dependency-name: attrs dependency-version: 25.4.0

- dependency-name: bcrypt dependency-version: 5.0.0

- dependency-name: black dependency-version: 25.9.0

- dependency-name: certifi dependency-version: 2025.10.5

- dependency-name: charset-normalizer dependency-version: 3.4.4

update-type: version-update:semver-patch

- dependency-name: click dependency-version: 8.3.0

- dependency-name: click-option-group dependency-version: 0.5.9

- dependency-name: cloudpickle dependency-version: 3.1.2

- dependency-name: deprecated dependency-version: 1.3.1

- dependency-name: discord-py dependency-version: 2.6.4

- dependency-name: dnspython dependency-version: 2.8.0

- dependency-name: email-validator dependency-version: 2.3.0

- dependency-name: executing dependency-version: 2.2.1

- dependency-name: fastapi dependency-version: 0.121.0

- dependency-name: fastapi-cli dependency-version: 0.0.14

- dependency-name: frozenlist dependency-version: 1.8.0

- dependency-name: gitpython dependency-version: 3.1.45

- dependency-name: greenlet dependency-version: 3.2.4

- dependency-name: httptools dependency-version: 0.7.1

- dependency-name: icecream dependency-version: 2.1.8

- dependency-name: idna dependency-version: '3.11'

- dependency-name: iniconfig dependency-version: 2.3.0

- dependency-name: isort dependency-version: 7.0.0

- dependency-name: markdown-it-py dependency-version: 4.0.0

- dependency-name: markupsafe dependency-version: 3.0.3

- dependency-name: multidict dependency-version: 6.7.0

- dependency-name: numpy dependency-version: 2.3.4

- dependency-name: nvidia-ml-py dependency-version: 13.580.82

- dependency-name: pandas dependency-version: 2.3.3

- dependency-name: platformdirs dependency-version: 4.5.0

- dependency-name: playwright dependency-version: 1.55.0

- dependency-name: propcache dependency-version: 0.4.1

- dependency-name: psutil dependency-version: 7.1.3

- dependency-name: psycopg dependency-version: 3.2.12

- dependency-name: psycopg-binary dependency-version: 3.2.12

- dependency-name: pydantic dependency-version: 2.12.3

- dependency-name: pydantic-core dependency-version: 2.41.4

- dependency-name: pydantic-settings dependency-version: 2.11.0

- dependency-name: pygments dependency-version: 2.19.2

- dependency-name: pylint dependency-version: 4.0.2

- dependency-name: pylint-plugin-utils dependency-version: 0.9.0

- dependency-name: pylint-pydantic dependency-version: 0.4.1

- dependency-name: python-dotenv dependency-version: 1.2.1

- dependency-name: python-gitlab dependency-version: 7.0.0

- dependency-name: python-semantic-release dependency-version: 10.4.1

- dependency-name: pyyaml dependency-version: 6.0.3

- dependency-name: requests dependency-version: 2.32.5

- dependency-name: rich dependency-version: 14.2.0

- dependency-name: rich-toolkit dependency-version: 0.15.1

- dependency-name: sqlalchemy dependency-version: 2.0.44

- dependency-name: starlette dependency-version: 0.50.0

- dependency-name: tomli dependency-version: 2.3.0

- dependency-name: typer dependency-version: 0.20.0

- dependency-name: typing-extensions dependency-version: 4.15.0

- dependency-name: typing-inspection dependency-version: 0.4.2

- dependency-name: uvicorn dependency-version: 0.38.0

- dependency-name: uvloop dependency-version: 0.22.1

- dependency-name: watchfiles dependency-version: 1.1.1

- dependency-name: wrapt dependency-version: 2.0.0

- dependency-name: yarl dependency-version: 1.22.0

dependency-group: production-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- Add dependabot configuration for automated dependency updates
  ([`b964e24`](https://github.com/milsman2/disc-golf-api/commit/b964e24a402bf3b68ff4873d2651e5146ce421c6))


## v0.14.1 (2025-10-31)

### Bug Fixes

- Add event results for league sessions 5 week 4, week 5, and week 6
  ([`0cadc31`](https://github.com/milsman2/disc-golf-api/commit/0cadc31a3bf2351f527041f4a1b3b7d7b003240a))


## v0.14.0 (2025-10-26)

### Bug Fixes

- Improve docstring formatting and clarity in CRUD modules for EventResult, Course, CourseLayout,
  and DiscEvent
  ([`c3c6529`](https://github.com/milsman2/disc-golf-api/commit/c3c6529ca9a3bf7439e294bc577efc994add86f7))

- Improve readability of API documentation and test case for event results
  ([`be57cbf`](https://github.com/milsman2/disc-golf-api/commit/be57cbfda3137569b66f0008cc4f02dd1912a558))

- Refactor code structure for improved readability and maintainability
  ([`0f42bb5`](https://github.com/milsman2/disc-golf-api/commit/0f42bb5415ba3f06f6aa6e6a5168ceb7ff5ad25e))

- Remove redundant datetime imports in test_partial_update_disc_event
  ([`908bc0d`](https://github.com/milsman2/disc-golf-api/commit/908bc0d5220a02d9a505094029aa35768509544b))

- Remove redundant imports and improve type hinting in event result and course layout modules
  ([`10672c1`](https://github.com/milsman2/disc-golf-api/commit/10672c18319bb32b6302cdb076c1f3213663c011))

- Reorder course_id and layout_id definitions in models for consistency
  ([`1418f46`](https://github.com/milsman2/disc-golf-api/commit/1418f4627ffd22f99844bb5eebaa52aa27873b78))

- Update data directory paths in disc_event_processing.py and round_processing.py for consistency
  ([`c9630c6`](https://github.com/milsman2/disc-golf-api/commit/c9630c67dda40495c1f5bec004cbbc7524824c74))

- Update down_revision in migration file to correct reference
  ([`a593aff`](https://github.com/milsman2/disc-golf-api/commit/a593aff0777a5506ad8cc02d6fae4851c4db2a1c))

### Chores

- Remove outdated Excel files for Jester HFDS league sessions
  ([`ce9251c`](https://github.com/milsman2/disc-golf-api/commit/ce9251cd29d2573409361b76f5227f0ae01dc4df))

- Uv package updates
  ([`36c2f79`](https://github.com/milsman2/disc-golf-api/commit/36c2f7938a31dc41425d9b967c13866a3389d4c5))

### Features

- Add partial update functionality for disc events and enhance related schemas
  ([`c01941a`](https://github.com/milsman2/disc-golf-api/commit/c01941a96c68085710efbb65a56636ff717e1d0e))

- Implement grouping of event results by division with sorting options
  ([`b1809bc`](https://github.com/milsman2/disc-golf-api/commit/b1809bc3eb00bd3a35f2655a45ca175b54f57950))


## v0.13.0 (2025-09-02)

### Bug Fixes

- Clean up import statements in pre_start.py and enhance structure in round_processing.py
  ([`45ac1fe`](https://github.com/milsman2/disc-golf-api/commit/45ac1fe412c3051e7921045f71907f86f19ec3cc))

- Correct sample CSV path in test_event_result.py
  ([`33e0cba`](https://github.com/milsman2/disc-golf-api/commit/33e0cba281193c3af466600d75bcdd9084250743))

- Improve readability of sample CSV path in test_event_result.py
  ([`ad7b185`](https://github.com/milsman2/disc-golf-api/commit/ad7b1859579e00e6f9ff110925134b253f23121a))

- Refine error handling in CSV processing and database initialization
  ([`aed203e`](https://github.com/milsman2/disc-golf-api/commit/aed203e31dbd1b919b939da0f7b2429f841fd08e))

### Features

- Add event results CSV and update event session processing functions
  ([`7f5492c`](https://github.com/milsman2/disc-golf-api/commit/7f5492cd707f14b130a2df69a449cd5c1477d2e4))


## v0.12.0 (2025-08-20)

### Code Style

- Format get_aggregated_event_results route definition for consistency
  ([`cb932aa`](https://github.com/milsman2/disc-golf-api/commit/cb932aa59ba91026e525f24aa61fecc3ad736ecc))

### Features

- Add aggregated event results endpoint and median round score calculations
  ([`4dfc52b`](https://github.com/milsman2/disc-golf-api/commit/4dfc52ba2a63de28db7870df3cc6cc2bbe5ee9eb))

- Add median round score calculations and schemas for event results
  ([`d906907`](https://github.com/milsman2/disc-golf-api/commit/d906907601acd748ee4f587240c3453e63c00a2a))


## v0.11.1 (2025-08-16)

### Bug Fixes

- Add event results for session 3
  ([`15ac5f3`](https://github.com/milsman2/disc-golf-api/commit/15ac5f38d5629c53123dc1dabb1b2982edd205fb))


## v0.11.0 (2025-08-13)

### Bug Fixes

- Centralize SQLAlchemy engine configuration and pool settings in config
  ([`4d481d0`](https://github.com/milsman2/disc-golf-api/commit/4d481d0d793f60b6284b4152b7b8b7b7d3ae1c04))

- Add `engine_kwargs` computed property to `Settings` for environment-based SQLAlchemy engine
  options (pool_size, max_overflow, pool_timeout). - Refactor `db.py` to use
  `**settings.engine_kwargs` for engine creation, enabling config-driven pool management. - Minor
  docstring formatting cleanup in Locust

### Features

- Switch Dockerfile to Gunicorn for FastAPI sync code; add Locust event results test and dev
  dependency
  ([`d32033c`](https://github.com/milsman2/disc-golf-api/commit/d32033c585d36d04cd48a157cd9c1c7fe8ae4186))

- Update Dockerfile to use Gunicorn with Uvicorn worker for better multi-core utilization in sync
  FastAPI deployments. - Add `locust_tests/locust_event_results.py` with documentation and a basic
  load test for event results endpoint. - Add Locust as a dev dependency in pyproject.toml for
  easier load testing


## v0.10.0 (2025-08-10)

### Bug Fixes

- Correct formatting and import order in event session handling
  ([`18f4176`](https://github.com/milsman2/disc-golf-api/commit/18f4176abfa13f3dac6f27a7dbf61f10b96544c4))

- Merge branch 'main' into feat/event-session-processing
  ([`78c41e3`](https://github.com/milsman2/disc-golf-api/commit/78c41e3bf516c2ec95eda556b5b004f673bb74e9))

### Features

- Add event session name uniqueness check and update related tests
  ([`38750a1`](https://github.com/milsman2/disc-golf-api/commit/38750a127d524d8c41d21d3c0be33c9e52cc79b3))

- Implemented a check in the event session creation route to prevent duplicate names. - Updated test
  cases to validate the uniqueness of event session names. - Refactored test fixtures and improved
  data handling in tests for clarity.


## v0.9.4 (2025-08-09)

### Bug Fixes

- Update tag name for event sessions in API router
  ([`64f5de0`](https://github.com/milsman2/disc-golf-api/commit/64f5de0679ef760ce0d03c83c6a880c9f1cee398))

### Features

- Add event session processing and retrieval by session ID
  ([`c93152e`](https://github.com/milsman2/disc-golf-api/commit/c93152ed3b8256e8bf5c759a888eda323d2ac412))

- Implemented comprehensive error handling in event session posting. - Added functionality to
  process all JSON files in the specified directory. - Introduced new API endpoint to retrieve event
  results by event session ID. - Added tests for retrieving event results by session ID. - Created
  new event session JSON file for testing.


## v0.9.3 (2025-08-09)

### Bug Fixes

- Add event results for TC Jester HFDS League Sessions 2
  ([`bfcbc33`](https://github.com/milsman2/disc-golf-api/commit/bfcbc334d9c67c381a9019aec9d637bd958eb87f))


## v0.9.2 (2025-08-07)

### Bug Fixes

- Remove sensitive information from debug output in pre_start.sh
  ([`935680c`](https://github.com/milsman2/disc-golf-api/commit/935680cf92dd34d68f10aade640b5965f6a4801e))


## v0.9.1 (2025-08-07)

### Bug Fixes

- Remove POSTGRES_PASSWORD echo for security reasons
  ([`b7f3608`](https://github.com/milsman2/disc-golf-api/commit/b7f3608df60043d1164f04dd847419eb0873072f))


## v0.9.0 (2025-08-07)

### Bug Fixes

- Format docstring for test_get_event_results_by_username function
  ([`ee2d20f`](https://github.com/milsman2/disc-golf-api/commit/ee2d20fab7b4780f9659b30aa90d28f694400669))

### Features

- Add functionality to retrieve event results by username
  ([`12ef871`](https://github.com/milsman2/disc-golf-api/commit/12ef8717359ccc77e60147ef8143bfe86dc9383b))


## v0.8.2 (2025-08-06)

### Bug Fixes

- Update .dockerignore to include additional ignored files
  ([`b7d357e`](https://github.com/milsman2/disc-golf-api/commit/b7d357ef4eefe3d1ecf29f48d44ddf8d1b1f0ca3))


## v0.8.1 (2025-08-04)

### Bug Fixes

- Remove outdated event results Excel files
  ([`2d61777`](https://github.com/milsman2/disc-golf-api/commit/2d6177793194ae9708eaef0337474c2eb9fa5073))


## v0.8.0 (2025-08-03)

### Bug Fixes

- Correct router import name for course layouts and add course layouts routes
  ([`1ca6b72`](https://github.com/milsman2/disc-golf-api/commit/1ca6b7254bb1c8412cd343ec0ff37d0b3cdffef3))

- Correct router import name for courses and update __all__ declaration
  ([`f659054`](https://github.com/milsman2/disc-golf-api/commit/f659054f5d0dbd4eefa5c0108ef8fa573e1b44fc))

- Correct string formatting in event session ID retrieval and adjust import order in main API module
  ([`b40c741`](https://github.com/milsman2/disc-golf-api/commit/b40c741c23beccb786e1e4905746846d13de8af9))

- Remove trailing slashes from API endpoint URLs in tests
  ([`55102a1`](https://github.com/milsman2/disc-golf-api/commit/55102a165b0a3f4e7325ad07ba16f77ea2a5dc24))

- Remove unnecessary blank lines in course layouts, courses, and event sessions route files
  ([`9e206ea`](https://github.com/milsman2/disc-golf-api/commit/9e206ea66ff3a2d0a862a4bfed9559f592d70363))

- Rename course router import and update __all__ declaration
  ([`faa845e`](https://github.com/milsman2/disc-golf-api/commit/faa845e1a062bf2f61f83d1ba4327c7418cf76ae))

- Update API endpoint paths for event sessions to use hyphenated format
  ([`1658979`](https://github.com/milsman2/disc-golf-api/commit/165897984c627e5ee002df663584b4318b7deae1))

- Update dependencies for aiohttp, aiosignal, fastapi, and starlette versions
  ([`8164b06`](https://github.com/milsman2/disc-golf-api/commit/8164b06adf4987e1399cc9f7dcfe0ad75445e2fe))

- Update login route paths for access and test token endpoints
  ([`914454b`](https://github.com/milsman2/disc-golf-api/commit/914454b8391f8ecd0c103928137f11cf9e5d97bf))

- Update pytest command to run all tests in the pytests directory
  ([`67aa247`](https://github.com/milsman2/disc-golf-api/commit/67aa2473574011fe734423ce3042d48aa77139f4))

- Update status codes for various routes and adjust response models
  ([`feaff2b`](https://github.com/milsman2/disc-golf-api/commit/feaff2bfc0d314f007dc4f47a98e96b8b4839729))

### Features

- Add course retrieval by name and update course model handling
  ([`46ecc98`](https://github.com/milsman2/disc-golf-api/commit/46ecc984fa334f74494378526e8791230fe35a74))

- Implement event session ID retrieval and enhance CSV processing logic
  ([`f2abd3c`](https://github.com/milsman2/disc-golf-api/commit/f2abd3c452778e25e5f228ce10f8a8da162b9027))

- Update API routes to include 'id' in path for courses, course layouts, event results, and event
  sessions
  ([`3dc6492`](https://github.com/milsman2/disc-golf-api/commit/3dc64922d979ada17f909a2948f8bd4ee2cf2744))


## v0.7.0 (2025-07-13)

### Features

- Update Docker configuration to use 'uv run' for application startup
  ([`182d571`](https://github.com/milsman2/disc-golf-api/commit/182d571c4631f9b2358f9892aab6df7805d622f6))


## v0.6.0 (2025-07-11)

### Features

- Migrate to uv for Python package management
  ([`ba35f82`](https://github.com/milsman2/disc-golf-api/commit/ba35f82a29e95ec2532e622d4879347eb89d6d3c))

- Replace pip and requirements.txt with uv for faster dependency resolution - Update Dockerfile to
  use uv sync --frozen for reproducible builds - Update GitHub Actions workflow to use uv run
  commands - Improve build performance and dependency management consistency


## v0.5.8 (2025-07-08)

### Bug Fixes

- Correct formatting in docstrings for test functions in event result and session tests
  ([`1693fb2`](https://github.com/milsman2/disc-golf-api/commit/1693fb2b6e5e53958e9c97d8d2a606402d8d4f2d))

- Update docstring formatting for test_valid_event_result_with_layouts function
  ([`380b7e0`](https://github.com/milsman2/disc-golf-api/commit/380b7e0c053893827b0c7951d48c68b7502fc487))

### Refactoring

- Update codebase to replace references from league sessions to event sessions
  ([`1b0b230`](https://github.com/milsman2/disc-golf-api/commit/1b0b230ca32731ecf6c69d1a1b0193ea3b20a4b2))


## v0.5.7 (2025-07-02)

### Bug Fixes

- Ensure CMD in Dockerfile has a newline at the end for proper execution
  ([`de9cbc4`](https://github.com/milsman2/disc-golf-api/commit/de9cbc4a506bbcd3fa48c44f4e9bf929fc949e5d))


## v0.5.6 (2025-07-02)

### Bug Fixes

- Correct POSTGRES_USER environment variable to use POSTGRES_OWNER
  ([`7083945`](https://github.com/milsman2/disc-golf-api/commit/7083945a1ce39c0ccd0418e89237689fa4ea0e7a))


## v0.5.5 (2025-06-27)

### Bug Fixes

- Update .pylintrc to ignore CHANGELOG.md for Pylint checks
  ([`6375e1c`](https://github.com/milsman2/disc-golf-api/commit/6375e1ca7be09c5cbf820cc8aecd189438392a26))


## v0.5.4 (2025-06-27)

### Bug Fixes

- Clean up whitespace and formatting in test files for consistency
  ([`b24d516`](https://github.com/milsman2/disc-golf-api/commit/b24d516a533397f497c2b361ae572cd28ce8ee82))

- Refactor course tests to use consistent test client and session fixtures
  ([`aecd398`](https://github.com/milsman2/disc-golf-api/commit/aecd398d012fe6557e843ee56c9f9f8a5b5a2dea))

- Rename get_all_courses function to test_get_all_courses for consistency
  ([`fab5e08`](https://github.com/milsman2/disc-golf-api/commit/fab5e0805070061d037a7c993fe7f10dad02fd15))

- Rename session fixture to test_session_fixture for clarity
  ([`155454b`](https://github.com/milsman2/disc-golf-api/commit/155454b19c666cd5a883179ddd7cb97ebae85c3f))


## v0.5.3 (2025-06-25)

### Bug Fixes

- Clean up test code by adding missing newlines and formatting adjustments
  ([`5a252bd`](https://github.com/milsman2/disc-golf-api/commit/5a252bdc03038fdf653d8a3d14b1e3b72a97e296))

- Enhance event result tests and add league session validation
  ([`40c4012`](https://github.com/milsman2/disc-golf-api/commit/40c40128c2d315a8c8003ecf5949548dd0a57168))

- Improve error message formatting for league session validation in create_event_result_route
  ([`200e315`](https://github.com/milsman2/disc-golf-api/commit/200e3153f1bc74208edebcb7a22ce587ece4aa45))

- Improve formatting and documentation in test_event_result.py
  ([`2fc8879`](https://github.com/milsman2/disc-golf-api/commit/2fc887989340318ae36756e17107f465131e53ce))

- Refactor test fixtures to use consistent naming for sample client and league session ID
  ([`4d77230`](https://github.com/milsman2/disc-golf-api/commit/4d772307f56070038f8101065f25d0493d8861bf))

- Remove redundant import statement for league_session
  ([`496c348`](https://github.com/milsman2/disc-golf-api/commit/496c3488b4b10c766d025f070893b974bd0459a2))


## v0.5.2 (2025-06-25)

### Bug Fixes

- Add wait loop for Postgres readiness before database setup
  ([`28ce506`](https://github.com/milsman2/disc-golf-api/commit/28ce50686c66ffcb88635dc6369f5ee9c20a07c8))


## v0.5.1 (2025-06-25)

### Bug Fixes

- Remove version declaration from Docker Compose file
  ([`8b4df45`](https://github.com/milsman2/disc-golf-api/commit/8b4df45c5f6e1757bc2ffc678059fe8e0f9b7230))


## v0.5.0 (2025-06-24)

### Bug Fixes

- Update PostgreSQL port mapping and remove Redis service from Docker Compose
  ([`ced677b`](https://github.com/milsman2/disc-golf-api/commit/ced677b8c1dffe268ee877736c03fb23713a2c87))

### Features

- Add Docker Compose configuration for PostgreSQL and Redis services
  ([`421f837`](https://github.com/milsman2/disc-golf-api/commit/421f83797dfd69a50f26780b212b343a40dfa0d2))


## v0.4.0 (2025-06-21)

### Features

- Enhance database setup in pre_start.sh and add POSTGRES_OWNER to config
  ([`af4af2f`](https://github.com/milsman2/disc-golf-api/commit/af4af2f8eb72b1005b8d7eed96fd69b0eac139cb))


## v0.3.1 (2025-06-19)

### Bug Fixes

- Add push trigger for main branch in release workflow
  ([`8cf6125`](https://github.com/milsman2/disc-golf-api/commit/8cf6125f2f7b6d0da7234cd313cdf66a08bc470f))

- Update package versions in requirements.txt for compatibility and improvements
  ([`c361ea1`](https://github.com/milsman2/disc-golf-api/commit/c361ea179608e3cb0058c50a3be27bdf5569c246))


## v0.3.0 (2025-06-13)

### Bug Fixes

- Improve docstring formatting for clarity in league session API tests
  ([`4c15f79`](https://github.com/milsman2/disc-golf-api/commit/4c15f7940f3d27babcb7530a592ffa01c610f608))

- Remove outdated requests package from requirements.txt
  ([`5f6f74e`](https://github.com/milsman2/disc-golf-api/commit/5f6f74ea615115d1b9f6dc34dcd612718de6dc2d))

- Update league session dates and enhance league session API test assertions
  ([`7ff207e`](https://github.com/milsman2/disc-golf-api/commit/7ff207ea42c96ef978b9f98aa217d0b3397c8b65))

- Update module docstring for clarity on league session API tests
  ([`08aa2f8`](https://github.com/milsman2/disc-golf-api/commit/08aa2f813224ea2778a872a25360df9fd626b7d7))

- Update package versions in requirements.txt for compatibility and improvements
  ([`f3e6a89`](https://github.com/milsman2/disc-golf-api/commit/f3e6a896d5cf7c3f9f9521c762687c136744a75b))

### Features

- Add league session management functionality
  ([`55db535`](https://github.com/milsman2/disc-golf-api/commit/55db535f47ed11932d3b9e2f31ae65cc76589ea6))

- Introduced new API routes for managing league sessions, including creation, retrieval, updating,
  and deletion. - Implemented CRUD operations for league sessions in the database. - Created
  Pydantic schemas for validating and serializing league session data. - Updated event results to
  associate them with league sessions. - Added new league session JSON data for testing. - Enhanced
  round processing to include points assignment based on player positions. - Created migration
  scripts to set up the league_sessions table and update event_results schema. - Added unit tests
  for league session API endpoints.


## v0.2.5 (2025-06-04)

### Bug Fixes

- Update round_processing to debug point values.
  ([`f8604c5`](https://github.com/milsman2/disc-golf-api/commit/f8604c514586dc78c684177bde7fbb841aecc602))


## v0.2.4 (2025-05-27)

### Bug Fixes

- Enable container scanning
  ([`3697afc`](https://github.com/milsman2/disc-golf-api/commit/3697afc2803981d72c6a5bec5396d77ce34f75a6))


## v0.2.3 (2025-05-27)

### Bug Fixes

- Update image due to broken dockerfile
  ([`5ea29db`](https://github.com/milsman2/disc-golf-api/commit/5ea29dbdeb7d5b6cb6bcb41e1ddb930995e4617f))


## v0.2.2 (2025-05-27)

### Bug Fixes

- Add test for deleting course and refactor Courses to match
  ([`ef52929`](https://github.com/milsman2/disc-golf-api/commit/ef5292995d8173a7726ec892490b7a5f9fd0a95e))

- Remove unnecessary f-string
  ([`b1544b1`](https://github.com/milsman2/disc-golf-api/commit/b1544b13e034225a5677bd10f502deb11ddefa22))

- Update Dockerfile per rec
  ([`adac348`](https://github.com/milsman2/disc-golf-api/commit/adac348239269a9338281d132dfe10ee5bdfb4f0))

- Update Dockerfile.
  ([`979d455`](https://github.com/milsman2/disc-golf-api/commit/979d455e208fc6351f7a8786d820eb399b42b912))

- Update documentation
  ([`ca5e66d`](https://github.com/milsman2/disc-golf-api/commit/ca5e66d8b81160b9c5b5e77e7eea544f46e429ec))


## v0.2.1 (2025-05-17)

### Bug Fixes

- Add date and unique constraint to date for event_result
  ([`7cc1546`](https://github.com/milsman2/disc-golf-api/commit/7cc154631bd44cf9f030b509f3b3824d7ed875fe))

- Allow GET for multiple event_results
  ([`04c60b4`](https://github.com/milsman2/disc-golf-api/commit/04c60b47217ea2e5a4c925173d5a919ae334a201))

- Automate getting date for event_result
  ([`9322ce5`](https://github.com/milsman2/disc-golf-api/commit/9322ce53ef638ed3e7360ffbf503d58a26931428))

- Corrected expected response code for new course POST
  ([`76d2a68`](https://github.com/milsman2/disc-golf-api/commit/76d2a68fec29f27d1a611e9ac70a2e62e8186328))

- Working pytest for new event_result data shape
  ([`3933a65`](https://github.com/milsman2/disc-golf-api/commit/3933a65ab2dde8e5347cf441b26402b50b71d45b))


## v0.2.0 (2025-05-13)

### Bug Fixes

- Able to post rounds
  ([`d1bf4b4`](https://github.com/milsman2/disc-golf-api/commit/d1bf4b4dad3ae1b096e4674dbef4e326f1c12f6e))

- Add course data processing and POST script
  ([`e74f74f`](https://github.com/milsman2/disc-golf-api/commit/e74f74ff2e0a574007752499abdf68e51eae60a9))

- Add loop for processing all csv files.
  ([`9e72cd3`](https://github.com/milsman2/disc-golf-api/commit/9e72cd3f0531649c0ea4ba72198e793956faec83))

- Add points and testing for points.
  ([`88b8b2f`](https://github.com/milsman2/disc-golf-api/commit/88b8b2f009e39275a0339c4470ce7c9ee3e0977d))

- Add psycopg[binary] for postgresql
  ([`b33502b`](https://github.com/milsman2/disc-golf-api/commit/b33502b7dccab5dce6ff061b0a3f326f7f68b56a))

- Apply isort and refactor startup.
  ([`ea639bc`](https://github.com/milsman2/disc-golf-api/commit/ea639bc916442694fb3d36f50805a55897e9e80f))

- Better typing and cleanup.
  ([`f708e05`](https://github.com/milsman2/disc-golf-api/commit/f708e05a63f36f13c4e894b1bebf30ffc6bb3321))

- Black formatting
  ([`c5eccb8`](https://github.com/milsman2/disc-golf-api/commit/c5eccb81c9c10325c79048d3fb4b24b2d809cf16))

- Pylint cleaning.
  ([`992f290`](https://github.com/milsman2/disc-golf-api/commit/992f2905937da56db31d2ed3865f4dd27cac991a))

- Pylint nit pick.
  ([`1929839`](https://github.com/milsman2/disc-golf-api/commit/1929839a5f49f3c51fe6355272cc0f0c12238ea5))

- Reorder bash scripts
  ([`f458267`](https://github.com/milsman2/disc-golf-api/commit/f458267abfea87be40e766be1b9289fd48a877da))

- Reorganize sample data
  ([`8aeae0f`](https://github.com/milsman2/disc-golf-api/commit/8aeae0fab8247b63d586a2da49ba725e892a476b))

- Update sample data location
  ([`bc7f06a`](https://github.com/milsman2/disc-golf-api/commit/bc7f06a99305de8a34f604faef384032484fd890))


## v0.1.0 (2025-04-30)

### Bug Fixes

- Allow module wide use of db
  ([`b8f5f85`](https://github.com/milsman2/disc-golf-api/commit/b8f5f8518400d7633153beb8a2cba0be372d16d3))

- Call out correct test.
  ([`138ac97`](https://github.com/milsman2/disc-golf-api/commit/138ac97e4f3c57e7d7209588e616e1646fae661b))

- Make sure database is in working shape.
  ([`3d9e430`](https://github.com/milsman2/disc-golf-api/commit/3d9e430622ede2dc12ee7a7298b14d427ad24b5f))

- Modify event_result schemas
  ([`4ef9709`](https://github.com/milsman2/disc-golf-api/commit/4ef9709729ae8a3a1d56ee7b711e013ead2ec323))

- Refactoring
  ([`e87e8dc`](https://github.com/milsman2/disc-golf-api/commit/e87e8dca5c261e88d4206b3cf1691a519bf6c440))

- Working pytest for event_results
  ([`fec3dfd`](https://github.com/milsman2/disc-golf-api/commit/fec3dfd84fdd2aff2f2e3af02690c8dd52d54843))


## v0.0.6 (2025-04-28)


## v0.0.5 (2025-04-26)


## v0.0.4 (2025-04-25)

### Bug Fixes

- Always run a test build on every commit to make sure build is green.
  ([`08a6c5c`](https://github.com/milsman2/disc-golf-api/commit/08a6c5c44e11eaa299db5d1ef762dbf6ccec884a))


## v0.0.3 (2025-04-23)

### Bug Fixes

- Add event_result routes, CRUD and sqlalchemy models.
  ([`0547224`](https://github.com/milsman2/disc-golf-api/commit/05472240fa53f878017c623fbaad6e9caffced4b))

- Add event_results to course_layout ORM model.
  ([`ef3f978`](https://github.com/milsman2/disc-golf-api/commit/ef3f9784c038602d423933de14d62bd58a68b3f8))

- Add standalone run to build and test.
  ([`b897b07`](https://github.com/milsman2/disc-golf-api/commit/b897b07a9534995c4354cc93aef07ab9c72be517))

- Add testing for event_result post route.
  ([`1fe6f86`](https://github.com/milsman2/disc-golf-api/commit/1fe6f86ad8aef1dc3691066b832b05eb143b0ad5))

- Make all tests pass with sample data.
  ([`c9373a0`](https://github.com/milsman2/disc-golf-api/commit/c9373a09278386397f83ba57e5c78e0dafe925c5))

- Make everything sqlite compatible.
  ([`6a667db`](https://github.com/milsman2/disc-golf-api/commit/6a667db0a60f34f44bea6b469baae5a5cf58eb94))

- Passing event result create
  ([`2511f24`](https://github.com/milsman2/disc-golf-api/commit/2511f24bdbc846b2974eab5e120515b342a98c3b))

- Run all tests.
  ([`3203673`](https://github.com/milsman2/disc-golf-api/commit/32036736b9c7b6834e97c54ea633c67f86da9a21))

### Chores

- Add alembic revision for new table.
  ([`a8d1612`](https://github.com/milsman2/disc-golf-api/commit/a8d1612aa04297c83129d5dd603144e658d5d99b))

- Add module docstring for course_layout ORM model.
  ([`0ac2dac`](https://github.com/milsman2/disc-golf-api/commit/0ac2dacbef7db9a140a198e54fe04e617c506120))

### Features

- **models, schemas**: Add EventResult model and Pydantic schemas with Course and CourseLayout
  relationships
  ([`1ab8b72`](https://github.com/milsman2/disc-golf-api/commit/1ab8b72552bbb48beb1105c9d58604a0667818bb))


## v0.0.2 (2025-03-27)


## v0.0.1 (2025-03-27)

### Chores

- Update pip.
  ([`79bda7a`](https://github.com/milsman2/disc-golf-api/commit/79bda7af0820f3f4724298529989bd2e0f3bf16a))


## v0.0.0 (2025-03-27)

### Continuous Integration

- Update GitHub Actions release workflow
  ([`198e4dd`](https://github.com/milsman2/disc-golf-api/commit/198e4dd10127ae99c68fba72b769af9143a403ac))
