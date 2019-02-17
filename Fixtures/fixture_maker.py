from collections import deque


def make_fixtures(num_teams, times_to_play):
    current_played = 0
    team_nums = list(range(num_teams))
    fixtures = {i + 1: [] for i in team_nums}
    while current_played < times_to_play:
        team_nums = deque(list(range(num_teams)))
        for i in range(num_teams - 1):
            start_idx = i % 2
            for home, away in zip(team_nums[0::2], team_nums[1::2]):
                team_num_a = home + 1
                team_num_b = away + 1
                fixtures[team_num_a].append('{}{}'.format(team_num_b, 'H' if start_idx else 'A'))
                fixtures[team_num_b].append('{}{}'.format(team_num_a, 'A' if start_idx else 'H'))
                start_idx = not start_idx
            # team_nums.append(team_nums.pop(0))
            team_nums.rotate(2)
        current_played += 1

    return fixtures
