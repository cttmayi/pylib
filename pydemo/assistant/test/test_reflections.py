
from typing import List, Dict, Any


REFLECTIONS = '''\
You will be given the history of a past experience in which you were placed in an environment and given a task to complete.
You were unsuccessful in completing the task. Do not summarize your environment, but rather think about the strategy and path you took to attempt to complete the task.
Devise a concise, new plan of action that accounts for your mistake with reference to specific actions that you should have taken.
For example, if you tried A and B but forgot C, then devise a plan to achieve C with environment-specific actions.
You will need this later when you are solving the same task. Give your plan after "Plan". Here are two examples:

'''

FEW_SHOT_EXAMPLES = '''\

'''


def _get_scenario(s: str) -> str:
    """Parses the relevant scenario from the experience log."""
    return s.split("Here is the task:")[-1].strip()

def _generate_reflection_query(log_str: str, memory: List[str]) -> str:
    scenario: str = _get_scenario(log_str)
    plan_from_past = ''

    if len(memory) > 0:
        plan_from_past += 'Plans from past attempts:\n'
        for i, m in enumerate(memory):
            plan_from_past += f'Trial #{i}: {m}\n'

    query: str = f"""\
{REFLECTIONS}
{FEW_SHOT_EXAMPLES}

{scenario}

{plan_from_past}

New plan:"""

    return query



class EnvironmentHistory:
    def __init__(self, base_query: str, start_info, memory: List[str], history: List[Dict[str, str]] = []) -> None:
        base_prompt = 'Interact with a household to solve a task. Here are two examples.\n' + d[f'react_{v}_1'] + d[f'react_{v}_0']
        self._cur_query: str = f'{_get_base_query(base_query, start_info, memory)}'
        self._history: List[Dict[str, str]] = history
        self._last_action: str = ''
        self._is_exhausted: bool = False

    def add(self, label: str, value: str) -> None:
        assert label in ['action', 'observation', 'human_edit']
        self._history += [{
            'label': label,
            'value': value,
        }]
        if label == 'action':
            if value == self._last_action:
                self._is_exhausted = True
            else:
                self._last_action = value

    def check_is_exhausted(self) -> bool:
        return self._is_exhausted

    def reset(self) -> None:
        self._history = []

    def __str__(self) -> str:
        s: str = self._cur_query + '\n'
        for i, item in enumerate(self._history):
            if item['label'] == 'action':
                s += f'> {item["value"]}'
            elif item['label'] == 'observation':
                s += item['value']
            # NOT CURRENTLY SUPPORTED
            elif item['label'] == 'human_edit':
                s += f'[human edit]: {item["value"]}'
            if i != len(self._history) - 1:
                s += '\n'
        return s

def _get_base_query(base_query: str, start_info: str, memory: List[str]) -> str:
    query = base_query

    # add memory if it exists
    if len(memory) > 0:
        query += '\n\nYour memory for the task below:'
        for i, m in enumerate(memory):
            query += f'\nTrial {i}:\n{m.strip()}'
    query += f"\nHere is the task:\n{start_info}"
    return query