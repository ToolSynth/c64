10 rem ***** stress test for emulator *****
20 print "starting stress test..."
30 print "1) nested for/next loops (intensive arytmetyka)"
40 t1 = ti
41 print "before loop"
50 for i=1 to 200
51   print "first loop: "; i
60   for j=1 to 200
70     d = i * j  : rem proste mnozenie, obciazy cpu w petli
80   next j
90 next i
100 t2 = ti : rem odczyt systemowego timera
110 print "   -> petle 200x200 zakonczone. czas (ticks): "; t2-t1
120 print : print "2) test operacji na tablicach stringowych"
130 dim a$(500) : rem przykladowa tablica 500 lancuchow
140 for k=1 to 500
150   a$(k) = "line_" + str$(k)
160 next k
170 t1 = ti
180 for k=1 to 500
190   x$ = a$(k)
200 next k
210 t2 = ti
220 print "   -> odczyt 500 elementow. czas (ticks): "; t2-t1
230 print : print "3) drukowanie tablicy (obciazenie print i ekranu)"
240 print "   (moze troche potrwac...)"
250 t1 = ti
260 for k=1 to 500
270   print a$(k)
280 next k
290 t2 = ti
300 print : print "   -> drukowanie zakonczone. czas (ticks): "; t2-t1
310 print : print "stress test zakonczony!"
320 end