EMPTY_PROJECT = ""
EMPTY_DESCRIPTION = ""


class Task:
    def __init__(self, id: int) -> None:
        self.id = id
        self.project = EMPTY_PROJECT
        self.description = EMPTY_DESCRIPTION

    def load(self, description: str) -> None:
        task_info = description.split(":")
        if len(task_info) > 1:
            self.project = task_info[0].strip()
            self.description = ":".join(task_info[1:]).strip()
        else:
            self.project = EMPTY_PROJECT
            self.description = description.strip()

    def get_full_description(self) -> str:
        if len(self.project) > 0:
            return f"[{self.project}] {self.description} ({self.id})"
        else:
            return f"{self.description} ({self.id})"

    def build_to_save_str(self) -> str:
        if len(self.project) > 0:
            return f"{self.project}: {self.description}"
        else:
            return f"{self.description}"

    def __repr__(self) -> str:
        return f"T({self.get_full_description()})"
