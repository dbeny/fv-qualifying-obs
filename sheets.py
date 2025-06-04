import time
import requests
import tempfile
import openpyxl
from io import BytesIO
from openpyxl.utils import range_boundaries
from tqdm import tqdm

def format_time(t):
    if not t:
        return ""
    return f"{t.minute:02}:{t.second:02}.{int(t.microsecond / 1000):03}"

def format_gap(t):
    if not t:
        return ""
    total_seconds = t.minute * 60 + t.second + t.microsecond / 1_000_000
    return f"+{total_seconds:.3f}"

def convert_onedrive_link(url):
    if "redir" in url or "download" in url:
        return url
    if ":x:/" in url:
        return url.replace(":x:/", ":x:/download.aspx?")
    if "?" in url:
        return url + "&download=1"
    return url + "?download=1"

def download_excel(url):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            chunk_size = 8192
            buffer = BytesIO()
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading Excel") as pbar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    buffer.write(chunk)
                    pbar.update(len(chunk))
            buffer.seek(0)
            return buffer
    except Exception as e:
        print("Download failed:", e)
        return None

def read_range(wb_data, sheet_name, cell_range):
    try:
        wb = openpyxl.load_workbook(wb_data, data_only=True)
        ws = wb[sheet_name]
        min_col, min_row, max_col, max_row = range_boundaries(cell_range)
        formatted_rows = []
        for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
            raw = [cell.value for cell in row]
            driver = raw[0]
            team = raw[1]
            gap = format_gap(raw[3])
            fastest = format_time(raw[4])
            formatted_rows.append([driver, team, fastest, gap])
        return formatted_rows

    except Exception as e:
        print("Excel read error:", e)
        return []