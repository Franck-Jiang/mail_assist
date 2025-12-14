from datetime import datetime
import locale

def format_datetime(string_date: str) -> datetime:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Linux / macOS
    dt = datetime.strptime(string_date[9:].strip().encode("utf-8").decode("latin1"), "%A %d %B %Y %H:%M") # 'Envoyé : xxxxxxxxxxxx\r'
    return dt

if __name__ == "__main__":
    str_date = "mardi 30 mars 2025 23:36"
    print(format_datetime(str_date))