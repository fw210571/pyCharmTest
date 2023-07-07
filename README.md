## Setup

1.  `git clone <project_url>`
1.  `python3 -m pip install --upgrade pip`
1.  `pip install pipenv`
1.  To activate this project's virtualenv firsttime, run the following:

        pipenv shell

1.  Install the dependencies

        pipenv install --dev

1.  Install a new production package

        pipenv install <package_name>

1.  Install a new development package

        pipenv install <package_name> --dev

1.  Find all outdated packages

        pipenv update --outdated

1.  Update packages

        pipenv update OR pipenv update <package_name>

## Running the tests

        pytest -v -s -n <number_of_workers> --browser=chrome --client=levelup --env=production --logging=DEBUG --headless=false
