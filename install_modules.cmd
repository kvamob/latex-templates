@echo off

d:
cd \GIT-REPOS\latex-templates

pip3 install virtualenv
virtualenv venv

call venv\Scripts\Activate

pip3 install jinja2

pause