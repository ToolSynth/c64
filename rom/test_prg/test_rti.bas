10 print "ustawienie adresu procedury obsługi przerwania"
20 poke 56320, 12
30 data 40, 96
40 for i = 0 to 1 : read a : poke 49152 + i, a : next i
50 print "wygenerowano przerwanie"
60 end