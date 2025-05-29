from strategies.high_priority import HighPriorityStrategy
from strategies.normal_priority import NormalPriorityStrategy

def get_strategy(priority: str):
    if priority.lower() == 'high':
        return HighPriorityStrategy()
    return NormalPriorityStrategy()
