from pathlib import Path


class PathBuilder:
    def build(self, root_dir: str, filename: str) -> str:
        if root_dir and filename:
            home_path = Path(root_dir)
            if home_path.exists():
                if home_path.is_dir():
                    return f"{root_dir}/.config/{filename}"
                else:
                    raise Exception(f"{root_dir} is a file. Directory is required.")
            else:
                raise Exception(f"{root_dir} does not exist")
        else:
            raise Exception(f"empty value for the required directory or file (dir: {root_dir}, file: {filename})")
