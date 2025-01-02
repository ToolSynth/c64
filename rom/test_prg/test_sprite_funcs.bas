10 print "test sprite'ow na c64"
20 poke 53280, 0 : poke 53281, 0 : rem czarny ekran i ramka

30 rem === definicja sprite'a w pamięci ===
40 for i = 0 to 62 : read a : poke 12288 + i, a : next i
50 poke 2040, 192  : rem adres sprite'a (192 = 12288 / 64)

60 rem === ustawienie sprite'a ===
70 poke 53248, 100 : poke 53249, 100  : rem pozycja x=100, y=100
80 poke 53269, 1   : rem włącz sprite 0
90 poke 53287, 2   : rem kolor sprite'a = czerwony
100 poke 53271, 1  : rem tryb wielokolorowy sprite'ów
110 poke 53285, 3  : rem kolor dodatkowy dla sprite'ów
120 poke 53286, 6  : rem drugi kolor dla trybu wielokolorowego

270 rem === test kolizji sprite/sprite ===
280 print "test kolizji sprite/sprite..."
290 poke 53270, 3  : rem włączenie drugiego sprite'a
300 poke 53250, 110 : poke 53251, 100  : rem sprite 1 obok sprite'a 0
310 poke 53288, 7   : rem kolor sprite'a 1 = żółty
320 for i = 100 to 120
330   poke 53248, i
340   if peek(53278) > 0 then print "kolizja wykryta!"
350   for j = 1 to 50 : next j
360 next i
370 poke 53270, 1  : rem wyłączenie sprite'a 1

550 print "testy zakonczone!"

560 end

570 rem === dane bitmapy sprite'a (63 bajty) ===
580 data 0,0,0,24,24,24,60,60,60,126,126,126,219,219,219
590 data 255,255,255,60,36,60,24,24,24,24,24,24,24,24,24
600 data 24,24,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
610 data 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
