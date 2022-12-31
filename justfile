lint:
    python3 -m pylint */*.py main.py

run USER='lyubolp' AMOUNT='10':
    . .venv/bin/activate
    python3 main.py -u {{USER}} -t {{AMOUNT}}