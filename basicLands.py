def get_basics(playables_colors, basics_left):
    red, blue, green, white, black = 0, 0, 0, 0, 0
    here_be_basics = []
    total_basics = basics_left

    if not playables_colors: #if you are in colorless for some reason
        while basics_left > 0:
            here_be_basics.append('Wastes')
            basics_left -= 1
        return here_be_basics
    else: #else do normal basic land adding
        for i in playables_colors:
            for j in i:
                if j == 'R':
                    red += 1
                if j == 'B':
                    black += 1
                if j == 'G':
                    green += 1
                if j == 'U':
                    blue += 1
                if j == 'W':
                    white += 1

        red_f = red / (blue+green+black+white+red)
        blue_f = blue / (blue+green+black+white+red)
        green_f = green / (blue+green+black+white+red)
        black_f = black / (blue+green+black+white+red)
        white_f = white / (blue+green+black+white+red)

        red = round(red_f * basics_left)
        blue = round(blue_f * basics_left)
        green = round(green_f * basics_left)
        black = round(black_f * basics_left)
        white = round(white_f * basics_left)

        while red > 0:
            here_be_basics.append('Mountain')
            red -= 1
            basics_left -= 1
        while blue > 0:
            here_be_basics.append('Island')
            blue -= 1
            basics_left -= 1
        while green > 0:
            here_be_basics.append('Forest')
            green -= 1
            basics_left -= 1
        while black > 0:
            here_be_basics.append('Swamp')
            black -= 1
            basics_left -= 1
        while white > 0:
            here_be_basics.append('Plains')
            white -= 1
            basics_left -= 1

        if len(here_be_basics) > total_basics:
            here_be_basics.pop()

        return here_be_basics