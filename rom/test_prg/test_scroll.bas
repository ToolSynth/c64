10 print "test przełączania screen memory i banków vic"
20 for b=0 to 3
30 poke 56576, (peek(56576) and 252) or b : rem ustawienie banku vic
40 print "aktualny bank vic: "; b
50 end