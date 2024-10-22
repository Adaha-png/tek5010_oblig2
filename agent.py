import random

import numpy as np


class Agent:
    def __init__(self, speed=25, search_range=250):
        self.pos = np.random.rand(2) * 1000
        self.v = speed
        self.wait = 0
        self.w_max = 100
        self.c = 1
        self.di = np.random.rand() * 2 * np.pi
        self.search_range = search_range

    def move(self, tasks, agents):
        if self.wait <= 0:
            self.pos[0] += self.v * np.cos(self.di)
            self.pos[1] += self.v * np.sin(self.di)

            if not (0 < self.pos[0] < 1000) or not (0 < self.pos[1] < 1000):
                self.pos = np.clip(self.pos, a_min=0, a_max=1000)
                self.di = np.random.rand() * 2 * np.pi

            for t in tasks:
                if np.linalg.norm(self.pos - t.pos) <= t.r:
                    self.wait = max(
                        np.round(
                            (self.w_max * self.temperature(agents) ** 2)
                            / (self.temperature(agents) ** 2 + self.c)
                        ),
                        1,
                    )
                    self.di = (self.di + np.pi) % (2 * np.pi)
                    self.callout(agents)

                    break

        else:
            self.wait -= 1

    def move_with_auction(self, tasks, agents):
        if self.wait <= 0:
            self.pos[0] += self.v * np.cos(self.di)
            self.pos[1] += self.v * np.sin(self.di)

            if not (0 < self.pos[0] < 1000) or not (0 < self.pos[1] < 1000):
                self.pos = np.clip(self.pos, a_min=0, a_max=1000)
                self.di = np.random.rand() * 2 * np.pi

            for t in tasks:
                if np.linalg.norm(self.pos - t.pos) <= t.r:
                    self.wait = max(
                        np.round(
                            (self.w_max * self.temperature(agents) ** 2)
                            / (self.temperature(agents) ** 2 + self.c)
                        ),
                        1,
                    )
                    self.di = (self.di + np.pi) % (2 * np.pi)
                    self.auction(agents, t.capacity - 1)

                    break

        else:
            self.wait -= 1

    def temperature(self, agents):
        return len(
            [a for a in agents if np.linalg.norm(a.pos - self.pos) <= self.search_range]
        )

    def callout(self, agents):
        for a in agents:
            if np.linalg.norm(a.pos - self.pos) < self.search_range and a is not self:
                a.call(self)

    def auction(self, agents, n_agents):
        # Calculate the distance of each agent from self
        distances = [
            (a, np.linalg.norm(a.pos - self.pos)) for a in agents if a is not self
        ]

        # Sort agents by distance
        sorted_agents = sorted(distances, key=lambda x: x[1])

        closest_agents = sorted_agents[:n_agents]

        # Call the closest agents
        for agent, distance in closest_agents:
            if distance < self.search_range:
                agent.call(self)

    def call(self, agent):
        direction_vector = agent.pos - self.pos
        self.di = np.arctan2(direction_vector[1], direction_vector[0])


class Task:
    def __init__(self, capacity=1, radius=50):
        self.capacity = capacity
        self.pos = np.random.rand(2) * 1000
        self.r = radius

    def solve(self, agents):
        actors = []

        for a in agents:
            if np.linalg.norm(a.pos - self.pos) <= self.r:
                actors.append(a)
                if len(actors) >= self.capacity:
                    self.pos = np.random.rand(2) * 1000
                    for act in actors:
                        act.wait = 0
                    return True

        return False
