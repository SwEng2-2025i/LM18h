from strategies.base_strategy import BaseStrategy

class HighPriorityStrategy(BaseStrategy):
    def format_message(self, message):
        return f"[🔥 HIGH PRIORITY] {message}"
