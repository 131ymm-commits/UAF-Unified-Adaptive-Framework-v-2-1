@echo off
set /p TASK="Введи задачу для ИИ: "
python uaf_context_loader.py "%TASK%" > prompt.txt
echo Промпт сохранён в prompt.txt
