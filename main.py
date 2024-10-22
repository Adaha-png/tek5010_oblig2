import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from agent import Agent, Task


def simulate(agents, tasks, maxitr=100000):
    solved = 0
    moving = np.zeros(maxitr)
    for i in tqdm(range(maxitr)):
        for agent in agents:
            agent.move_with_auction(tasks, agents)
            moving[i] += agent.wait == 0

        for task in tasks:
            solved += task.solve(agents)

    return solved / maxitr, moving / len(agents)


if __name__ == "__main__":
    # capacities = [1, 3]
    # num_agents = [1, 3, 5, 10, 20, 30]
    # for c in capacities:
    #     solved = []
    #     for num in num_agents:
    #         agents = [Agent(search_range=0) for _ in range(num)]
    #         tasks = [Task(capacity=c) for _ in range(1)]
    #         solv, mov = simulate(agents, tasks)
    #         solved.append(solv)
    #         plt.plot(mov)
    #         plt.show()
    #
    #     plt.figure(figsize=(10, 6))
    #     bar_width = 0.8  # Width of the bars
    #     positions = range(len(num_agents))  # X-axis positions for the bars
    #     plt.bar(positions, solved, width=bar_width, color="blue")
    #     plt.xlabel("Number of Agents")
    #     plt.ylabel("Tasks Solved per iteration")
    #     plt.title("BEECLUSTesque solving tasks")
    #     plt.xticks(positions, num_agents)  # Set the positions and labels for x-ticks
    #     plt.grid(axis="y")
    #     plt.savefig(f"{c}_capacity.png")

    capacity = 3
    num_agents = 30
    search_ranges = [0, 100, 200, 300, 400, 600, 1000, 1400]
    num_tasks = 2
    solved = []
    for sr in search_ranges:
        agents = [Agent(search_range=sr) for _ in range(num_agents)]
        tasks = [Task(capacity=capacity) for _ in range(num_tasks)]
        solv, mov = simulate(agents, tasks)
        solved.append(solv)

    plt.figure(figsize=(10, 6))
    bar_width = 0.8  # Width of the bars
    positions = range(len(search_ranges))  # X-axis positions for the bars
    plt.bar(positions, solved, width=bar_width, color="blue")
    plt.xlabel("Communication distance")
    plt.ylabel("Tasks Solved per iteration")
    plt.title(f"Solving tasks with call-out")
    plt.xticks(positions, search_ranges)  # Set the positions and labels for x-ticks
    plt.grid(axis="y")
    plt.savefig(f"search_ranges.png")
