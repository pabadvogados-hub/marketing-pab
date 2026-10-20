@echo off
REM Trigger do Task Scheduler - rode 3x por semana (Seg/Qua/Sex)
cd /d "c:\AUTOMAÇÕES PAB"
py CONTEUDO\jusbrasil_writer.py >> CONTEUDO\execucoes.log 2>&1
