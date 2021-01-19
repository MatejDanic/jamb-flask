def calculate_score(dice_set, box_type):
    score = 0

    if box_type <= 6:
        score = dice_set.count(box_type) * (box_type)

    elif box_type == 7 or box_type == 8:
        score = sum(dice_set)

    elif box_type == 9:
        for dice in dice_set:
            if dice_set.count(dice) >= 3:
                score = 3 * dice + 10
                break

    elif box_type == 10:
        has_straight = True
        straight = [2, 3, 4, 5]
        for n in straight:
            if n not in dice_set:
                has_straight = False
        if has_straight:
            if 1 in dice_set:
                score = 35
            elif 6 in dice_set:
                score = 45

    elif box_type == 11:
        found_pair = False
        found_trips = False
        for dice in dice_set:
            if dice_set.count(dice) == 3 and not found_trips:
                score += 3 * dice
                found_trips = True
                continue
            elif dice_set.count(dice) == 2 and not found_pair:
                score += 2 * dice
                found_pair = True
                continue
        if not found_pair or not found_trips:
            score = 0
        else:
            score += 30

    elif box_type == 12:
        for dice in dice_set:
            if dice_set.count(dice) >= 4:
                score = 4 * dice + 40
                break

    elif box_type == 13:
        for dice in dice_set:
            if dice_set.count(dice) == 5:
                score = 5 * dice + 50
                break
    return score
