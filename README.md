# droxi_assignment

## Requirements

* Python (3.13) + pipenv virtual environment
* Java 8 or higher
* Node 2.21.0 or higher + npm package manager

## Installation

1. Install allure commandline by running `npm i -g allure-commandline`
2. Install the dependencies by running `pipenv install`
3. Activate the virtual environment by running `pipenv shell`

## Running tests

* In order to execute all test cases, run `pipenv run pytest`
* To run specific test, execute one of the following:

  * **API syncing**: `pipenv run pytest tests\cases\test_sync_api.py`
  * **API merging**: `pipenv run pytest tests\cases\test_sync_merge_api.py`
  * **UI specific card**: `pipenv run pytest tests\cases\test_card_ui.py`
  * **UI urgent cards**: `pipenv run pytest tests\cases\test_card_urgent_ui.py`

## Reports

The allure report is generated automatically after test completion.

Serve the report for browser view by running `allure serve reports/allure-results`.
