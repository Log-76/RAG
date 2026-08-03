from ..parsing import MinimalSource
from utils import error


def retrieve_data_from_minimal_source(self, data: MinimalSource) -> str:
    try:
        with open(data.file_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        if not raw_data:
            error(f"raw_data does not exist for {data.file_path}")
            return ""
    except Exception as e:
        error(f"error reading {data.file_path}: {e}")
        return ""
    try:
        return raw_data[data.first_character_index:
                        data.last_character_index]
    except Exception as e:
        error(f"error slicing {data.file_path}: {e}")
        return ""
