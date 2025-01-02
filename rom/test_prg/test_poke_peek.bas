10 print "test 3: poke/peek do ekranu"
20 screen = 1024 : rem adres początkowy ekranu tekstowego
30 poke screen, 65 : rem 'a'
40 poke screen+1, 66 : rem 'b'
50 poke screen+2, 67 : rem 'c'
60 print "zapisane: abc (poke)"
70 print "odczyt z ekranu (peek): ";
80 print chr$(peek(screen));chr$(peek(screen+1));chr$(peek(screen+2))
90 print "koniec testu 3"
100 end