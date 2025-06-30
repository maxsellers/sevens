import random
import time
#These are the teams - replace with DB info later
TEAM_A = "Team A"
TEAM_B = "Team B"
HALF_LENGTH = 7  # minutes per half
EVENTS = [
    "kickoff", "try", "conversion", "penalty", "turnover", "knock-on", "lineout", "scrum", "tackle"
]

def rng_event():
    # Weighted random events
    return random.choices(
        EVENTS,
        weights=[1, 3, 2, 1, 2, 1, 1, 1, 2],
        k=1
    )[0]

def simulate_half(team_a_score, team_b_score, play_by_play, half):
    possession = random.choice([TEAM_A, TEAM_B])
    time_left = HALF_LENGTH * 60  # total seconds in half
    play_by_play.append(f"--- Start of Half {half} ---")
    # Always start half with a kickoff
    kick_type, receiver, kickoff_outcome = kickoff_event(possession)
    minutes, seconds = divmod(time_left, 60)
    play_by_play.append(f"{minutes:02d}:{seconds:02d}: {possession} kicks off ({kick_type} kick). {receiver} receives.")
    possession = receiver
    event = ""
    # Advance time by 1-2 minutes (random seconds within that range)
    time_advance = random.randint(10, 30)
    time_left = max(0, time_left - time_advance)
    while time_left > 0:
        print(kickoff_outcome)
        if kickoff_outcome == "catch":
            catch_outcome, catch_step = catch_event(possession)
            event = catch_step
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {catch_outcome}")
        elif kickoff_outcome == "knock back":
            # play_by_play.append(f"{minutes:02d}:{seconds:02d}: {possession} knocks the ball back.")
            loose_ball_possession = loose_ball_event(possession)
            possession = loose_ball_possession
            event = "catch"
            # if "INTERCEPTED" in catch_outcome:
            #     play_by_play.append(f"{minutes:02d}:{seconds:02d}: Intercepted by {possession}")
            # play_by_play.append(f"{minutes:02d}:{seconds:02d}: {catch_outcome}")
        elif kickoff_outcome == "knock on":
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: Knock-on from kickoff by {possession}. Scrum awarded.")
            possession = TEAM_B if possession == TEAM_A else TEAM_A
            scrum_result, new_possession, next_event = scrum_event(possession)
            event = next_event
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {scrum_result}")
            possession = new_possession
        # event = rng_event()
        minutes, seconds = divmod(time_left, 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        kick_outcome = ""
        # if event == "kickoff":
        #     kick_type, receiver,kickoff_outcome = kickoff_event(possession)
        #     play_by_play.append(f"{timestamp}: {possession} kicks off ({kick_type} kick). {receiver} receives.")
        #     possession = receiver
        if event == "try":
            play_by_play.append(f"{timestamp}: {possession} scores a TRY!")
            if possession == TEAM_A:
                team_a_score += 5
            else:
                team_b_score += 5
            # Attempt conversion
            goal_kick_outcome, goal_kick_step = goal_kick_event(possession)
            play_by_play.append(f"{timestamp}: Conversion {goal_kick_outcome}")
            event = goal_kick_step
            if possession == TEAM_A:
                team_a_score += 2
            else:
                team_b_score += 2
            # After a try (and conversion), kickoff by the team that conceded the try
            kicking_team = TEAM_B if possession == TEAM_A else TEAM_A
            kick_type, receiver, kickoff_outcome = kickoff_event(kicking_team)
            play_by_play.append(f"{timestamp}: {kicking_team} kicks off ({kick_type} kick) after try. {receiver} receives.")
            possession = receiver
        # elif event == "penalty":
        #     play_by_play.append(f"{timestamp}: Penalty awarded to {possession}.")
        #     # 20% chance to kick for points
        #     if random.random() < 0.2:
        #         play_by_play.append(f"{timestamp}: {possession} kicks a PENALTY GOAL!")
        #         if possession == TEAM_A:
        #             team_a_score += 3
        #         else:
        #             team_b_score += 3
        elif event == "catch":
            catch_outcome, catch_step = catch_event(possession)
            play_by_play.append(f"{timestamp}: {catch_outcome}")
            event = catch_step
        elif event == "ruck":
            ruck_outcome, ruck_step = ruck_event(possession)
            play_by_play.append(f"{timestamp}: {ruck_outcome}")
            play_by_play.append(f"Ruck Step: {ruck_step}")
            event = ruck_step
        elif event == "turnover":
            play_by_play.append(f"{timestamp}: Turnover! Possession changes.")
            possession = TEAM_B if possession == TEAM_A else TEAM_A
        elif event == "lineout":
            play_by_play.append(f"{timestamp}: Lineout. {possession} throws in.")
        elif event == "loose_ball":
            loose_ball_possession = loose_ball_event(possession)
            play_by_play.append(f"{timestamp}: Loose ball! {loose_ball_possession} recovers.")
            possession = loose_ball_possession
            event = "catch"
        elif event == "scrum":
            scrum_result, new_possession, next_event = scrum_event(possession)
            event = next_event
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {scrum_result}")
            possession = new_possession
        elif event == "tackle":
            tackle_outcome, tackle_step = tackle_event(possession)
            play_by_play.append(f"{timestamp}: {tackle_outcome}")
            play_by_play.append(tackle_step)
            event = tackle_step
        elif event == "pass":
            pass_outcome, pass_step = pass_event(possession)
            event = pass_step
            play_by_play.append(f"{timestamp}: {pass_outcome}")
        elif event == "kick":
            kick_outcome, kick_step = kick_event(possession)
            play_by_play.append(f"{timestamp}: {kick_outcome}")
            event = kick_step
        elif event == "goal_kick":
            goal_kick_outcome, goal_kick_step = goal_kick_event(possession)
            play_by_play.append(f"{timestamp}: Goal Kick {goal_kick_outcome}")
            event = goal_kick_step
            if "misses" in goal_kick_outcome:
                possession = TEAM_B if possession == TEAM_A else TEAM_A
            elif possession == TEAM_A:
                team_a_score += 3
            else:
                team_b_score += 3
            
        elif event == "intercept":
            intercept_outcome, intercept_step = intercept_event(possession)
            play_by_play.append(f"{timestamp}: {intercept_outcome}")
            event = intercept_step
            if "tackled by sweeper" in intercept_outcome:
                possession = TEAM_B if possession == TEAM_A else TEAM_A
        # Advance time by 1-2 minutes (random seconds within that range)
        time_advance = random.randint(10, 30)  # 30 to 90 seconds
        time_left = max(0, time_left - time_advance)
    play_by_play.append(f"--- End of Half {half} ---")
    return team_a_score, team_b_score

def main():
    play_by_play = []
    team_a_score = 0
    team_b_score = 0

    team_a_score, team_b_score = simulate_half(team_a_score, team_b_score, play_by_play, 1)
    team_a_score, team_b_score = simulate_half(team_a_score, team_b_score, play_by_play, 2)

    play_by_play.append(f"FINAL SCORE: {TEAM_A} {team_a_score} - {TEAM_B} {team_b_score}")
    winner = TEAM_A if team_a_score > team_b_score else TEAM_B if team_b_score > team_a_score else "Draw"
    play_by_play.append(f"RESULT: {winner}")

    with open("play_by_play.txt", "w") as f:
        for line in play_by_play:
            f.write(line + "\n")

def kickoff_event(possession):
    # 50% chance for long or short kick
    kick_type = random.choice(["long", "short"])
    # Define odds for kick quality based on kick type
    if kick_type == "long":
        quality = random.choices(
            ["excellent", "good", "poor"],
            weights=[0.2, 0.6, 0.2]
        )[0]
        receiver_chance = {"excellent": 0.6, "good": 0.65, "poor": 0.75}[quality]
    else:  # short kick
        quality = random.choices(
            ["excellent", "good", "poor"],
            weights=[0.3, 0.5, 0.2]
        )[0]
        receiver_chance = {"excellent": 0.45, "good": 0.5, "poor": 0.55}[quality]

    # Determine which team receives
    if random.random() < receiver_chance:
        receiver = TEAM_B if possession == TEAM_A else TEAM_A
    else:
        receiver = possession

    # Determine kickoff outcome: catch, knock back, or knock on
    outcome = random.choices(
        ["catch", "knock back", "knock on"],
        weights=[0.7, 0.2, 0.1]
    )[0]

    # If knock on, possession changes to other team
    if outcome == "knock on":
        receiver = TEAM_B if receiver == TEAM_A else TEAM_A

    return f"{quality} {kick_type} ({outcome})", receiver, outcome
    
def catch_event(possession):
    # Simulate player decision: run, pass, or kick
    decision = random.choices(
        ["run", "pass", "kick"],
        weights=[0.5, 0.3, 0.2]
    )[0]
    if decision == "run":
        run_outcome, event = run_event(possession)
        return run_outcome, event
    elif decision == "pass":
        # 80% successful pass, 20% intercepted
        return f"{possession} offloads in the tackle and attempts a pass to a teammate.", "pass"
    else:  # kick
        return f"{possession} chooses to kick the ball.", "kick"

def run_event(possession):
    # Player can run into space, around marker, or through marker
    run_type = random.choices(
        ["into space", "around marker", "through marker"],
        weights=[0.4, 0.35, 0.25]
    )[0]
    if run_type == "into space":
        outcome = random.choices(
            ["breaks free", "tackled", "loses balance"],
            weights=[0.5, 0.4, 0.1]
        )[0]
    elif run_type == "around marker":
        outcome = random.choices(
            ["beats marker", "tackled", "forced out"],
            weights=[0.4, 0.5, 0.1]
        )[0]
    else:  # through marker
        outcome = random.choices(
            ["powers through", "tackled", "loses ball"],
            weights=[0.3, 0.6, 0.1]
        )[0]
    if outcome == "tackled":
        return f"{possession} runs {run_type} and is tackled.", "tackle"
    else:
        return run_vs_sweeper_event(possession)
    
def run_vs_sweeper_event(possession):
    # Player can run into space, around sweeper, or through sweeper
    run_type = random.choices(
        ["into space", "around sweeper", "through sweeper"],
        weights=[0.4, 0.35, 0.25]
    )[0]
    if run_type == "into space":
        outcome = random.choices(
            ["breaks free", "tackled by sweeper", "loses balance"],
            weights=[0.5, 0.4, 0.1]
        )[0]
    elif run_type == "around sweeper":
        outcome = random.choices(
            ["beats sweeper", "tackled by sweeper", "forced out"],
            weights=[0.4, 0.5, 0.1]
        )[0]
    else:  # through sweeper
        outcome = random.choices(
            ["powers through sweeper", "tackled by sweeper", "loses ball"],
            weights=[0.3, 0.6, 0.1]
        )[0]
    if outcome == "tackled by sweeper":
        return f"{possession} runs {run_type} and is tackled by the sweeper.", "tackle"
    else:
        return f"{possession} runs {run_type} and {outcome}.", "try"

def tackle_event(possession):
    # Tackle outcomes: pass, ruck, attacker knock-on, defender knock-on, penalty
    outcome = random.choices(
        ["pass", "ruck", "attacker_knock_on", "defender_knock_on", "penalty"],
        weights=[0.4, 0.3, 0.15, 0.05, 0.1]  # 10% chance for penalty
    )[0]
    if outcome == "pass":
        # 80% successful pass, 20% intercepted
        return f"{possession} offloads in the tackle and passes to a teammate.", "pass"
    elif outcome == "ruck":
        # 70% retained, 30% turnover
        if random.random() < 0.7:
            return f"Ruck formed. {possession} retains possession.", "ruck"
        else:
            other_team = TEAM_B if possession == TEAM_A else TEAM_A
            return f"Ruck formed. Turnover! {other_team} wins the ball.", "ruck"
    elif outcome == "attacker_knock_on":
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"{possession} knocks on in the tackle. Scrum awarded to {other_team}.", "scrum"
    elif outcome == "defender_knock_on":
        return f"Defender knocks on in the tackle. Scrum awarded to {possession}.", "scrum"
    else:  # penalty
        return f"Penalty awarded to {possession} at the tackle.", "goal_kick"
    
def loose_ball_event(possession):
    # 50/50 chance for attacker or defender to recover
    if random.random() < 0.5:
        winner = possession
    else:
        winner = TEAM_B if possession == TEAM_A else TEAM_A

    return winner

def scrum_event(possession):
    # Scrum feed can be excellent, good, or poor
    feed_quality = random.choices(
        ["excellent", "good", "poor"],
        weights=[0.2, 0.6, 0.2]
    )[0]
    event = "catch"
    new_possession = possession
    # Excellent: 70% retain, Good: 65% retain, Poor: 55% retain
    retain_chance = {"excellent": 0.7, "good": 0.65, "poor": 0.55}[feed_quality]
    # 5% chance for a penalty at the scrum
    if random.random() < 0.05:
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        outcome = f"Penalty at the scrum! Awarded to {other_team}."
        new_possession = other_team
    # 10% chance for a loose ball regardless of feed quality
    elif random.random() < 0.1:
        outcome = f"{possession} feeds the scrum ({feed_quality}). The ball comes loose!"
        event = "loose_ball"
    elif random.random() < retain_chance:
        outcome = f"{possession} feeds the scrum ({feed_quality}). Ball retained."
        new_possession = possession
    else:
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        outcome = f"{possession} feeds the scrum ({feed_quality}). Turnover! {other_team} wins the ball."
        new_possession = other_team
    return outcome, new_possession, event

def ruck_event(possession):
    # Possible outcomes: attackers secure, defenders secure, loose ball, penalty
    outcome = random.choices(
        ["attackers_secure", "defenders_secure", "loose_ball", "penalty"],
        weights=[0.5, 0.25, 0.1, 0.15]
    )[0]
    if outcome == "attackers_secure":
        return f"Ruck formed. {possession} secures the ball.", "catch"
    elif outcome == "defenders_secure":
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"Ruck formed. Turnover! {other_team} wins the ball.", "catch"
    elif outcome == "loose_ball":
        # winner = loose_ball_event(possession)
        return f"Ruck formed. The ball squirts loose!", "loose_ball"
    else:  # penalty
        return f"Penalty awarded to {possession} at the ruck.", "goal_kick", "goal_kick"

def pass_event(possession):
    # Possible outcomes: catch, intercept, forward pass, loose ball, knock-on, deliberate knock-on (penalty)
    outcome = random.choices(
        ["catch", "intercept", "forward_pass", "loose_ball", "knock_on", "deliberate_knock_on"],
        weights=[0.65, 0.17, 0.02, 0.07, 0.07, 0.02]
    )[0]
    if outcome == "catch":
        if random.random() < 0.15:
            sweeper_result, event = run_vs_sweeper_event(possession)
            return f"{possession} completes the pass to a teammate, while defender tried to intercept. {sweeper_result}", event
        else:
            return f"{possession} completes the pass to a teammate.", "catch"
    elif outcome == "intercept":
            other_team = TEAM_B if possession == TEAM_A else TEAM_A
            return f"Intercepted! {other_team} grabs the pass.", "intercept"
    elif outcome == "forward_pass":
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"Forward pass by {possession}. Scrum awarded to {other_team}.", "scrum"
    elif outcome == "loose_ball":
        # winner = loose_ball_event(possession)
        return f"The ball is loose.", "loose_ball"
    elif outcome == "knock_on":
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"Knock-on by {possession} while passing. Scrum awarded to {other_team}.", "scrum"
    else:  # deliberate_knock_on
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"Deliberate knock-on by {other_team}. Penalty awarded to {possession}.", "goal_kick"

def intercept_event(possession):
    # 80% chance of successful intercept, 20% chance of failure
    return run_vs_sweeper_event(possession)

def kick_event(possession):
    # Simulate a kick event
    kick_type = random.choice(["long", "short", "goal"])
    if kick_type == "long":
        outcome = random.choices(
            ["excellent", "good", "poor"],
            weights=[0.2, 0.6, 0.2]
        )[0]
    elif kick_type == "short":  # short kick
        outcome = random.choices(
            ["excellent", "good", "poor"],
            weights=[0.3, 0.5, 0.2]
        )[0]
    else:  # goal kick
        return f"{possession} goes for a {kick_type} kick.", "goal_kick"
    return f"{possession} puts in a {outcome} {kick_type} kick.", "loose_ball"

def goal_kick_event(possession):
    # Simulate a goal kick event
    if random.random() < 0.6:
        return f"{possession} successfully kicks the goal.", "kick_off"
    else:
        return f"{possession} misses the goal kick.", "catch"
if __name__ == "__main__":
    main()