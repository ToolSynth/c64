10 print "raster interrupt test"
20 poke 53280,0 : poke 53281,0 : rem ustaw kolory obramowania i tła na czarny
30 rem ładowanie handlera przerwań do adresu $c100 (49408)
40 data 169,1,141,0,192,64 : rem a9 01 8d 00 c0 40 (lda #$01 ; sta $c000 ; rti)
50 for i=0 to 5: read a: poke 49408+i, a: next i
60 rem ustawienie wektora irq na $c100 (49408)
70 poke 812,0 : rem $0314 (low byte irq vector) = 0
80 poke 813,193 : rem $0315 (high byte irq vector) = 193 ($c1), razem $c100
90 rem ustawienie przerwania rastra na linię 100
100 poke 53298,100 : rem $d012 (raster low byte) = 100
110 poke 53299,0 : rem $d011 (raster high bit) = 0 (ponieważ 100 < 256)
120 rem włączenie przerwania rastra w rejestrze d01a
130 poke 53290, peek(53290) or 1 : rem ustaw bit 0 (raster interrupt enable)
140 rem wyczyszczenie flagi przerwania
150 poke 53273,0 : rem $d019 (interrupt flag register) = 0
160 rem wyczyszczenie flagi w pamięci
170 poke 49152,0 : rem $c000 (flaga przerwania) = 0
180 rem główna pętla programu
190 print "waiting for interrupt..."
200 if peek(49152)=1 then print "interrupt occurred!": poke 53280,2 : poke 49152,0
210 goto 190