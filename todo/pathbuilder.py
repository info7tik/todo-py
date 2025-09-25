

from genericpath import isdir
from pathlib import Path


class PathBuilder:
    def build(self,home_dir:str, filename:str)-> str:
        home_path = Path(home_dir)
        if home_path.exists():
            if home_path.is_dir():
                return f"{home_dir}/.config/{filename}"
            else:
                raise Exception(f"{home_dir} is a file. Directory is required.")
        else:
            raise Exception(f"{home_dir} does not exist")
