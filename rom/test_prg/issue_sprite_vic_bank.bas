10 poke 56576,0 : rem wybierz bank vic #0 (zakres $0000-$3fff)
20 for i=0 to 63: read a
30 poke 12288+i,a
35 next i
40 poke 53272,(peek(53272) and 252) : rem screen=$0400, font=$1000
60 poke 53269,1
70 rem ustaw pozycje sprite (x=$d000, y=$d001):
80 poke 53248,100 : poke 53249,50
100 poke 2040,12288/64

110 print "sprite w banku 0. nacisnij dowolny klawisz, aby przejsc dalej."
120 gosub 1000

130 print : print "przelaczamy vic na bank #2 ($8000-$bfff)..."
140 poke 56576,2   : rem ustaw bank vic #2
160 for i=0 to 63
165 read a
166 poke (32768+12288)+i, a
167 next i
180 poke 53248,140
185 poke 53249,100
200 poke 2040,(32768+12288)/64
210 print "sprite w banku 2. gotowe!"
220 end

1010 get a$: if a$="" then 1010
1020 return

rem ***** dane: 64 bajty definicji sprite *****
rem ten przykladowy wzor to 21 wierszy x 3 bajty = 63 + 1 bajt pusty.
rem po prostu "blok" w srodku sprite'a (linijki srodkowe = 255).

3000 data 0,0,0,0,0,0,0,0
3010 data 0,0,0,0,0,0,0,0
3020 data 0,0
   rem (razem 18 zer - gorna czesc pusta)

3030 data 255,255,255,255,255,255,255,255
3040 data 255,255,255,255,255,255,255,255
3050 data 255,255,255,255,255,255,255,255
3060 data 255,255,255
   rem (razem 27 x 255 - srodek wypelniony)

3070 data 0,0,0,0,0,0,0,0
3080 data 0,0,0,0,0,0,0,0
3090 data 0,0
   rem (18 zer - dol sprite'a)
3100 data 0
   rem (ostatni bajt 0)

