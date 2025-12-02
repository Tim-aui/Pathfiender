import logging
import os
from logging.handlers import RotatingFileHandler

print(f"DEBUG [logger.py]: СКРИПТ ЗАПУЩЕН")
print(f"DEBUG [logger.py]: Текущая рабочая директория (os.getcwd()): {os.getcwd()}")
print(f"DEBUG [logger.py]: Полный путь к этому файлу (__file__): {os.path.abspath(__file__)}")

try:
    current_file_path = os.path.abspath(__file__)
    project_root_dir = os.path.dirname(os.path.dirname(current_file_path))
    logs_dir = os.path.join(project_root_dir, 'logs')

    print(f"DEBUG [logger.py]: Рассчитанный корень проекта: {project_root_dir}")
    print(f"DEBUG [logger.py]: Рассчитанная директория для логов: {logs_dir}")

    if not os.path.exists(logs_dir):
        print(f"DEBUG [logger.py]: Директория '{logs_dir}' не существует. Попытка создать...")
        os.makedirs(logs_dir)
        print(f"DEBUG [logger.py]: Директория '{logs_dir}' УСПЕШНО СОЗДАНА.")
    else:
        print(f"DEBUG [logger.py]: Директория '{logs_dir}' УЖЕ СУЩЕСТВУЕТ.")
 
    if os.access(logs_dir, os.W_OK):
        print(f"DEBUG [logger.py]: Есть права на ЗАПИСЬ (W_OK) в директорию '{logs_dir}'.")
    else:
        print(f"ERROR [logger.py]: НЕТ прав на ЗАПИСЬ (W_OK) в директорию '{logs_dir}'.")

except Exception as e:
    print(f"ERROR [logger.py]: ОШИБКА при создании/проверке директории логов '{logs_dir if 'logs_dir' in locals() else 'N/A'}': {e}")

app_logger_name = 'pathfiender'
main_app_logger = logging.getLogger(app_logger_name)

log_file_path = os.path.join(logs_dir if 'logs_dir' in locals() else project_root_dir, 'pathfiender.log') 
print(f"DEBUG [logger.py]: Полный путь к файлу лога: {log_file_path}")

file_handler = None
try:
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=5*1024*1024, 
        backupCount=5,
        encoding='utf-8' 
    )
    print(f"DEBUG [logger.py]: RotatingFileHandler для '{log_file_path}' УСПЕШНО СОЗДАН.")
except Exception as e:
    print(f"ERROR [logger.py]: ОШИБКА при создании RotatingFileHandler для '{log_file_path}': {e}")

active_handlers = [logging.StreamHandler()]
if file_handler:
    active_handlers.append(file_handler)
    print(f"DEBUG [logger.py]: FileHandler будет добавлен в basicConfig.")
else:
    print(f"WARNING [logger.py]: FileHandler не был создан или не будет добавлен. Логирование в файл ОТКЛЮЧЕНО.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=active_handlers
)

print("DEBUG [logger.py]: logger.py executed and configured!")


def get_logger(name: str = None) -> logging.Logger:
    if name:
        return logging.getLogger(f'{app_logger_name}.{name}')
    return main_app_logger