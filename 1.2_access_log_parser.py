import sys

if len(sys.argv) < 2:
    raise ValueError("Please provide log file name as an argument")

filename = sys.argv[1]
user_agents = {}

with open(filename, "r") as file:
    for line in file:
        parts = line.strip().split('"')

        if len(parts) >= 6:
            user_agent = parts[5]

            if user_agent in user_agents:
                user_agents[user_agent] += 1
            else:
                user_agents[user_agent] = 1

print(f"Total number of different user agents: {len(user_agents)}")
print("Number of requests per user agent:")

for agent, count in user_agents.items():
    print(f"{agent}: {count} requests")