1. на windows -  (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
1. на mac/linux -  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
2. переместиться в корень проекта
3. poetry install
4. poetry run python dowload_photos/main.py
