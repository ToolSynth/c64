10 poke 53280,0
15 poke 53281,0  :rem ustaw kolory tła i ramki na czarne
20 sc1=1024
21 sc2=2048 :rem adresy pamięci ekranu
30 for i=0 to 100
31 poke sc1+i,65+((i and 25))
35 next i
40 for i=0 to 100
41 poke sc2+i,90-((i and 25))
45 next i  :rem wypełnianie drugiego ekranu
50 poke 53272,(peek(53272) and 240) or 8 :rem ustawienie drugiego ekranu
60 for t=1 to 1000
61 next t :rem czekanie
75 PRINT "Nowy ekran aktywny!"
70 end