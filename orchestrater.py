import openai
from concurrent.futures import ThreadPoolExecutor

class Agent:
    def __init__(self, name):
        self.name = name

class TaskDivider(Agent):
    def divide_and_distribute_task(self, large_task):
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": f"Divide this task into smaller subtasks to be solved by other agents. First write a field with general context for all agents regardless of task this field should be prepended by [MT] and should be 1 - 3 sentences. Prepend a subtask to be solved with [SB(task_number)]: {large_task}"}]
        )
        divided_response = response.choices[0].message['content'].strip().split('\n\n')
        mt_field = divided_response[0]  # Extracting the MT field
        tasks = divided_response[1:]   # Extracting the subtasks

        # Prepending MT field to each task
        tasks_with_mt = [mt_field + "\n" + task for task in tasks]
        print(f"{self.name} divided the task into subtasks: {tasks_with_mt}")

        # Using ThreadPoolExecutor to distribute tasks to solvers
        with ThreadPoolExecutor(max_workers=len(tasks_with_mt)) as executor:
            futures = [executor.submit(solve_task, task) for task in tasks_with_mt]
            for future in futures:
                print(future.result())

def solve_task(task):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system", "content": f"Solve the task prepend: {task}"}]
    )
    solution = response.choices[0].message['content'].strip()
    print(f"Solved task: {task} as {solution}")
    return solution

def main():
    orchestrator = TaskDivider("TaskDivider")

    with open('input.txt', 'r') as file:
        large_task = file.read()

    orchestrator.divide_and_distribute_task(large_task)

if __name__ == "__main__":
    main()
