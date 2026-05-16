import logging
import logging.handlers
from pathlib import Path

# Корень проекта (два уровня вверх от этого файла)
BASE_DIR = Path(__file__).resolve().parent.parent

# Директория для лог-файлов
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Форматтер — используем все основные атрибуты LogRecord
VERBOSE_FORMAT = (
    "[%(asctime)s] "          # дата и время
    "%(levelname)-8s "        # уровень (выровнен по 8 символов)
    "%(name)s "               # имя логера (модуль)
    "%(module)s."             # имя файла без расширения
    "%(funcName)s:"           # имя функции
    "%(lineno)d "             # номер строки
    "| PID:%(process)d "      # PID процесса
    "TID:%(thread)d "         # ID потока
    "| %(message)s"           # само сообщение
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """
    Настраивает глобальное логирование.

    Часть 1: basicConfig — базовый вывод в файл app.log.
    Часть 2: корневой логер получает три хэндлера:
        console           → stderr
        rotating_file     → logs/app.log        (ротация по размеру)
        timed_file        → logs/app_daily.log  (ротация раз в сутки)
    """

    # basicConfig (требование задания)

    logging.basicConfig(
        level=logging.INFO,
        filename=LOGS_DIR / "basic.log",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt=DATE_FORMAT,
        encoding="utf-8",
    )

    # Форматтер

    formatter = logging.Formatter(fmt=VERBOSE_FORMAT, datefmt=DATE_FORMAT)

    # Хэндлер 1 — Консольный (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Хэндлер 2 — Файл с ротацией по размеру (RotatingFileHandler)
    # maxBytes=5 MB, backupCount=3 (храним app.log, app.log.1, .2, .3)
    rotating_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "app.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(formatter)

    # Хэндлер 3 — Файл с ротацией по времени (TimedRotatingFileHandler)
    # when='midnight' — ротация каждый день в полночь
    # backupCount=7   — хранить 7 дней логов
    timed_handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOGS_DIR / "app_daily.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    timed_handler.setLevel(logging.WARNING)  # в daily пишем только WARNING+
    timed_handler.setFormatter(formatter)
    timed_handler.suffix = "%Y-%m-%d"        # суффикс файла: app_daily.log.2025-05-16

    # ------------------------------------------------------------------
    # Корневой логер — подключаем все хэндлеры
    # ------------------------------------------------------------------
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Не дублируем хэндлеры при повторном вызове (актуально при hot-reload)
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(rotating_handler)
        root_logger.addHandler(timed_handler)
    else:
        # basicConfig уже добавил FileHandler — добавляем только новые
        existing_types = {type(h) for h in root_logger.handlers}
        if logging.StreamHandler not in existing_types:
            root_logger.addHandler(console_handler)
        if logging.handlers.RotatingFileHandler not in existing_types:
            root_logger.addHandler(rotating_handler)
        if logging.handlers.TimedRotatingFileHandler not in existing_types:
            root_logger.addHandler(timed_handler)

    # Сторонние библиотеки — не спамить DEBUG-сообщениями
    logging.getLogger("django").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
