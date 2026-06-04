#!/bin/bash
echo "Введи задачу для ИИ:"
read TASK
python uaf_context_loader.py "$TASK" > prompt.txt
echo "Промпт сохранён в prompt.txt"
