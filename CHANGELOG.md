# CHANGELOG


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
