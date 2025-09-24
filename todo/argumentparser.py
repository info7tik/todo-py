class ArgUmentParser:
    def __init__(self, script_args: list[str]) -> None:
        self.raw_args = script_args

    def command(self) -> str:
        if len(self.raw_args) == 0:
            return "list"
        else:
            return self.raw_args[0]

    def content(self) -> str:
        if len(self.raw_args) > 1:
            return " ".join(self.raw_args[1:])
        else:
            return ""

    def contentAsNumber(self) -> int:
        assert len(self.raw_args) == 2, f"content with number must look like 'command number'"
        return int(self.raw_args[1])

    def contentAsStringAndNumber(self) -> tuple[int, str]:
        assert len(self.raw_args) == 3, f"content with number must look like 'command string number'"
        return (int(self.raw_args[1]), self.raw_args[2])
