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
    time_advance = random.randint(30, 90)
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
            if "INTERCEPTED" in catch_outcome:
                play_by_play.append(f"{minutes:02d}:{seconds:02d}: Intercepted by {possession}")
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {catch_outcome}")
        elif kickoff_outcome == "knock on":
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: Knock-on from kickoff by {possession}. Scrum awarded.")
            possession = TEAM_B if possession == TEAM_A else TEAM_A
            scrum_result, new_possession = scrum_event(possession)
            event = "catch"
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {scrum_result}")
            possession = new_possession
        # event = rng_event()
        minutes, seconds = divmod(time_left, 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
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
            if random.random() < 0.6:
                play_by_play.append(f"{timestamp}: {possession} makes the CONVERSION.")
                if possession == TEAM_A:
                    team_a_score += 2
                else:
                    team_b_score += 2
            else:
                play_by_play.append(f"{timestamp}: {possession} misses the conversion.")
            # After a try (and conversion), kickoff by the team that conceded the try
            kicking_team = TEAM_B if possession == TEAM_A else TEAM_A
            kick_type, receiver, kickoff_outcome = kickoff_event(kicking_team)
            play_by_play.append(f"{timestamp}: {kicking_team} kicks off ({kick_type} kick) after try. {receiver} receives.")
            possession = receiver
        elif event == "penalty":
            play_by_play.append(f"{timestamp}: Penalty awarded to {possession}.")
            # 20% chance to kick for points
            if random.random() < 0.2:
                play_by_play.append(f"{timestamp}: {possession} kicks a PENALTY GOAL!")
                if possession == TEAM_A:
                    team_a_score += 3
                else:
                    team_b_score += 3
        elif event == "catch":
            catch_outcome, catch_step = catch_event(possession)
            play_by_play.append(f"{timestamp}: {catch_outcome}")
            event = catch_step
            if catch_step == "intercept":
                possession = TEAM_B if possession == TEAM_A else TEAM_A
        elif event == "turnover":
            play_by_play.append(f"{timestamp}: Turnover! Possession changes.")
            possession = TEAM_B if possession == TEAM_A else TEAM_A
        elif event == "knock-on":
            play_by_play.append(f"{timestamp}: Knock-on by {possession}. Scrum awarded.")
            possession = TEAM_B if possession == TEAM_A else TEAM_A
        elif event == "lineout":
            play_by_play.append(f"{timestamp}: Lineout. {possession} throws in.")
        elif event == "scrum":
            scrum_result, new_possession = scrum_event(possession)
            play_by_play.append(f"{minutes:02d}:{seconds:02d}: {scrum_result}")
            possession = new_possession
        # elif event == "tackle":
        #     play_by_play.append(f"{timestamp}: Big tackle by {possession}!")
        # Advance time by 1-2 minutes (random seconds within that range)
        time_advance = random.randint(30, 90)  # 30 to 90 seconds
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
        if random.random() < 0.8:
            return f"{possession} passes successfully.", "pass"
        else:
            return f"{possession} attempts a pass but it's INTERCEPTED!", "intercept"
    else:  # kick
        # 70% good kick, 30% poor kick
        if random.random() < 0.7:
            return f"{possession} puts in a good kick downfield.", "kick"
        else:
            return f"{possession} attempts a kick but it's charged down!", "charge_down"

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
        tackle_result = tackle_event(possession)
        return f"{possession} runs {run_type} and is tackled. {tackle_result}", "tackle"
    else:
        sweeper_result, event = run_vs_sweeper_event(possession)
        if "tackled by sweeper" in sweeper_result:
            tackle_result = tackle_event(possession)
            return f"{possession} runs {run_type} and is tackled by the sweeper. {tackle_result}", event
        else:            
            return f"{possession} runs {run_type} and {sweeper_result}.", event
    
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
        tackle_result = tackle_event(possession)
        return f"{possession} runs {run_type} and is tackled by the sweeper. {tackle_result}", "tackle"
    else:
        return f"{possession} runs {run_type} and {outcome}.", "try"

def tackle_event(possession):
    # Tackle outcomes: pass, ruck, attacker knock-on, defender knock-on, penalty
    outcome = random.choices(
        ["pass", "ruck", "attacker_knock_on", "defender_knock_on", "penalty"],
        weights=[0.4, 0.35, 0.15, 0.08, 0.02]  # 2% chance for penalty
    )[0]
    if outcome == "pass":
        # 80% successful pass, 20% intercepted
        if random.random() < 0.8:
            return f"{possession} offloads in the tackle and the pass is successful."
        else:
            return f"{possession} offloads in the tackle but it's INTERCEPTED!"
    elif outcome == "ruck":
        # 70% retained, 30% turnover
        if random.random() < 0.7:
            return f"Ruck formed. {possession} retains possession."
        else:
            other_team = TEAM_B if possession == TEAM_A else TEAM_A
            return f"Ruck formed. Turnover! {other_team} wins the ball."
    elif outcome == "attacker_knock_on":
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        return f"{possession} knocks on in the tackle. Scrum awarded to {other_team}."
    elif outcome == "defender_knock_on":
        return f"Defender knocks on in the tackle. Scrum awarded to {possession}."
    else:  # penalty
        return f"Penalty awarded to {possession} at the tackle."
    
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
    # Excellent: 70% retain, Good: 65% retain, Poor: 55% retain
    retain_chance = {"excellent": 0.7, "good": 0.65, "poor": 0.55}[feed_quality]
    # 10% chance for a loose ball regardless of feed quality
    if random.random() < 0.1:
        outcome = f"{possession} feeds the scrum ({feed_quality}). The ball comes loose!"
        loose_outcome, new_possession = loose_ball_event(possession)
        outcome += f" {loose_outcome[0]}"
    elif random.random() < retain_chance:
        outcome = f"{possession} feeds the scrum ({feed_quality}). Ball retained."
        new_possession = possession
    else:
        other_team = TEAM_B if possession == TEAM_A else TEAM_A
        outcome = f"{possession} feeds the scrum ({feed_quality}). Turnover! {other_team} wins the ball."
        new_possession = other_team
    return outcome, new_possession

if __name__ == "__main__":
    main()