# I have pirated this thing somewhere
blue_noise = """
    6f318ea271c347b1c932975e422555fc
    1963efde20fa9413266adcaac28a0da7
    7db24f0f41ad7b57d583f7177436e5d4
    29ca9884bd6835eca13e01b54df19344
    02f4385be605cc1cbb6590ce215cbe6b
    dfa47224d69c8b46f554e2307e9e1187
    53c415fe4c2db3730c28a969fdb0d33b
    64b4917aac61eb81d795c708481aee2c
    e81f450bcd3a12c1583c70dd8c567899
    d082f3a0e06e22f8a518eab834c6ab06
    6cbc335989ba9a4e2f86629d23f95f3f
    104bdb270043e479c5f0034a7f14e38f
    f6af77c8fb67920ed1ae6ddac052cba3
    1d5d9616a6b6371e5a402a8da839752e
    d8e93d8051edd9769fffb91bf2660485
    49bf09d22b600788e7500a7ce1cf9bb7
""".strip().split("\n    ")
for i, row in enumerate(blue_noise):
    blue_noise[i] = [int(row[j : j + 2], 16) for j in range(0, len(row), 2)]
