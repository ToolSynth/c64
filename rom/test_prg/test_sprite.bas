10 print "test rasterline + sprite: tło zmienia kolor"
20 poke 2040, 192 : rem wskaźnik sprite'a
30 poke 53269, 1 : rem włącz sprite 0
40 poke 53248, 160 : rem pozycja pozioma sprite'a
50 poke 53249, 100 : rem pozycja pionowa sprite'a
60 for i=0 to 63
70 poke 12288+i, 255 : rem sprite pełny prostokąt
80 next i
90 for x=160 to 220
100 poke 53248, x : rem przesuwanie sprite'a poziomo
110 wait 53266, 128 : rem czekaj na rasterline
120 poke 53280, (x mod 16) : rem zmiana koloru tła w zależności od pozycji sprite'a
130 next x
140 print "jeśli tło zmienia kolor podczas ruchu sprite'a, test zaliczony."
150 poke 53269, 0 : rem wyłącz sprite 0
150 end