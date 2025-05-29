from strategies.base_strategy import BaseStrategy

class NormalPriorityStrategy(BaseStrategy):
    def format_message(self, message):
        return f"[INFO] {message}"
