REM Install python virtualenv

virtualenv venv

REM Install requirements

call venv\Scripts\activate
pip install -r requirements.txt
call venv\Scripts\deactivate