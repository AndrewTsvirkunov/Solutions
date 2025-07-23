import datetime
from datetime import date
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup


# Базовый URL на случай относительных ссылок
BASE_URL = "https://spimex.com"

# Валидная часть пути
EXPECTED_PATH_PREFIX = "/upload/reports/oil_xls/oil_xls_"

def parse_page_links(html: str, start_date: date, end_date: date) -> List[Tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы.
    Возвращает список кортежей: (полная ссылка на файл, дата в имени файла)
    Parameters:
        html: HTML страницы;
        start_date: начальная дата фильтра;
        end_date: конечная дата фильтра.
    Returns:
        Список (URL, дата), если дата входит в заданный диапазон.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    results = []
    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]  # удаляем query-параметр (например ?utm...)

        if not is_valid_xls_link(href):
            continue

        file_date = extract_date_from_href(href)
        if not file_date:
            # TODO: вместо print можно логировать ошибку извлечения даты
            continue

        if start_date <= file_date <= end_date:
            full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
            results.append((full_url, file_date))
        else:
            # TODO: вместо print можно логировать ссылку вне диапазона
            pass

    return results


def is_valid_xls_link(href: str) -> bool:
    """
    Проверяет, соответствует ли ссылка ожидаемому шаблону
    Parameters:
        href: ссылка в виде строки
    Return:
        Ссылку начинающуюся на "/upload/reports/oil_xls/oil_xls_" и заканчивающуюся на ".xls".
    """
    return href.startswith(EXPECTED_PATH_PREFIX) and href.endswith(".xls")


def extract_date_from_href(href: str) -> Optional[date]:
    """
    Пытается извлечь дату из имени файла в ссылке.
    Возвращает None при ошибке.
    Parameters:
        href: ссылка в виде строки
    Return:
        Дату в формате datetime.date
    """
    try:
        date_str = href.split("oil_xls_")[1][:8]
        return datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except (IndexError, ValueError):
        return None