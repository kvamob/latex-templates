@echo off

chcp 1251 > nul
SET SRC_DIR="D:\GIT-REPOS\latex-templates\bhpassport"
SET DST_DIR="D:\Home System\���������\�������� �������\2023\_�������_"
chcp 866 > nul

cls
echo ################################################################################################

mkdir %DST_DIR%
mkdir %DST_DIR%\images

copy %SRC_DIR%\*.tex %DST_DIR% > nul
copy %SRC_DIR%\*.py %DST_DIR% > nul
copy %SRC_DIR%\images\* %DST_DIR%\images > nul

echo Source directory : %SRC_DIR%
echo Target directory : %DST_DIR%

echo ################################################################################################

rem ������� � ���������� ����� ����������
start "" %DST_DIR%

rem echo "Done..."

