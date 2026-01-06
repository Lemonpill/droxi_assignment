# droxi_assignment

## Requirements

* Python 3.13 + pipenv virtual environment
* Java 8 or higher (for report serving)
* Node 2.21.0 or higher + npm package manager (for report serving)

## Installation

1. Install allure commandline by running `npm i -g allure-commandline`
2. Install the dependencies by running `pipenv install`
3. Activate the virtual environment by running `pipenv shell`

## Running tests

* In order to execute all test cases, run `pipenv run pytest`
* To run specific test, execute one of the following:

  * **Sync Validation (Urgent Card Labeling)**: `pipenv run pytest tests\cases\test_api_urgent_card_labeling.py`
  * **Sync Validation (Merging)**: `pipenv run pytest tests\cases\test_api_merging.py`
  * **Specific Card Validation**: `pipenv run pytest tests\cases\test_gui_specific_card_validation.py`
  * **Urgent Cards Validation**: `pipenv run pytest tests\cases\test_gui_urgent_card_validation.py`

## Reports

The allure report is generated automatically after test completion.

Serve the report for browser view by running `allure serve reports/allure-results`.

**GH Actions**: Results are uploaded as artifacts and can be served locally.

## Environment variables

Environment variables required for GH Actions are stored in GH secrets.

The ones that are necessary for local execution will be attached to final deliverables zip.
