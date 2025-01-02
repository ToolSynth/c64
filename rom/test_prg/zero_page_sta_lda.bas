10 print "testy dla wielokrotnych adresów"
20 for a = 49408 to 49413 : rem testuj adresy $c100 - $c105
25 print "testing address "; a
30 for v = 0 to 255 : rem testuj wartości 0-255
35 print "  testing value "; v
40 poke a, v
50 r = peek(a)
60 if r <> v then print "failed: addr="; a; " val="; v; " read="; r : goto 100
70 next v
80 next a
90 print "wszystkie testy ok!" : end
100 print "testy zakończone z błędami." : end