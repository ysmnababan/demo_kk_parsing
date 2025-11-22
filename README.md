

python -m venv venv
source env/bin/activate


deactivate

pip install -r requirement.txt

pip freeze >> requirement.txt
