import re
import sys
from solution import AbstractSolution


class Solution(AbstractSolution):
    def process_input(self):
        self.r = {}
        self.n = {}
        self.id = {}
        self.N = 0
        for line in self.input:
            match = re.fullmatch(
                r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)",
                line,
            )
            if match is not None:
                valve = match.group(1)
                flow_rate = int(match.group(2))
                if flow_rate > 0:
                    self.r[valve] = flow_rate
                    self.id[valve] = self.N
                    self.N += 1
                self.n[valve] = match.group(3).split(", ")
            else:
                print("bad regex")
                sys.exit(-1)

    def total_flow(self, S):
        return sum(v for k, v in self.r.items() if S & (1 << self.id[k]))

    def solve(self, v, t, S, dp):

        if S == (1 << self.N) - 1:
            return self.total_flow(S) * t

        if t == 0:
            return 0

        if (v, t, S) in dp:
            return dp[(v, t, S)]

        dp[(v, t, S)] = max(self.solve(u, t - 1, S, dp) for u in self.n[v])

        if v in self.r and not (S & (1 << self.id[v])):
            dp[(v, t, S)] = max(
                dp[(v, t, S)], self.solve(v, t - 1, S ^ (1 << self.id[v]), dp)
            )

        dp[(v, t, S)] += self.total_flow(S)

        return dp[(v, t, S)]

    def solve2(self, v1, v2, t, S, dp):
        if t == 0:
            return 0

        if S == (1 << self.N) - 1:
            return self.total_flow(S) * t

        if (v1, v2, t, S) in dp:
            return dp[(v1, v2, t, S)]

        if (v2, v1, t, S) in dp:
            return dp[(v2, v1, t, S)]

        dp[(v1, v2, t, S)] = max(self.solve2(u, w, t-1, S, dp) for u in self.n[v1] for w in self.n[v2])

        if v1 in self.r and not (S & (1 << self.id[v1])):
            dp[(v1, v2, t, S)] = max(dp[(v1, v2, t, S)], max(self.solve2(v1, w, t-1, S ^ (1 << self.id[v1]), dp) for w in self.n[v2]))

        if v2 in self.r and not (S & (1 << self.id[v2])):
            dp[(v1, v2, t, S)] = max(dp[(v1, v2, t, S)], max(self.solve2(u, v2, t-1, S ^ (1 << self.id[v2]), dp) for u in self.n[v1]))

        if (v1 in self.r and not (S & (1 << self.id[v1]))) and (v2 in self.r and not (S & (1 << self.id[v2]))):
            dp[(v1, v2, t, S)] = max(dp[(v1, v2, t, S)], self.solve2(v1, v2, t-1, S ^ (1 << self.id[v1]) ^ (1 << self.id[v2]), dp))

        dp[(v1, v2, t, S)] += self.total_flow(S)

        dp[(v2, v1, t, S)] = dp[(v1, v2, t, S)]

        return dp[(v1, v2, t, S)]


    def part1(self):
        pass
        # return self.solve("AA", 30, 0, {})


    def part2(self):
        return self.solve2("AA", "AA", 26, 0, {})


def main():
    print("Sample: ")
    solution = Solution("./resources/day16/sample.txt")
    solution.print_answers()

    # print()
    # print("Real input: ")
    # solution = Solution("./resources/day16/input.txt")
    # solution.print_answers()


if __name__ == "__main__":
    main()
