10 print "raster interrupt test"
20 poke 53280,0 : poke 53281,0 : rem ustaw kolory obramowania i tła na czarny

30 rem ładowanie handlera przerwań do adresu $c100 (49408)
40 poke 49408,169 : rem a9 (lda #$01)
50 poke 49409,1   : rem #$01
60 poke 49410,141 : rem 8d (sta $c000)
70 poke 49411,0   : rem $00 (adres $c000)
80 poke 49412,192 : rem c0 (sta $c000)
90 poke 49413,64  : rem 40 (rti)

100 rem ustawienie wektora irq na $c100 (49408)
110 poke 812,0     : rem $0314 (low byte irq vector) = 0
120 poke 813,193   : rem $0315 (high byte irq vector) = 193 ($c1), razem $c100

130 rem ustawienie przerwania rastra na linię 100
140 poke 53298,100 : rem $d012 (raster low byte) = 100
150 poke 53299,0   : rem $d011 (raster high bit) = 0 (ponieważ 100 < 256)

160 rem włączenie przerwania rastra w rejestrze d01a
170 poke 53290, peek(53290) or 1 : rem ustaw bit 0 (raster interrupt enable)

180 rem wyczyszczenie flagi przerwania w rejestrze d019
190 poke 53273,0   : rem $d019 (interrupt flag register) = 0

200 rem wyczyszczenie flagi w pamięci
210 poke 49152,0   : rem $c000 (flaga przerwania) = 0

220 rem główna pętla programu
230 print "waiting for interrupt..."
240 if peek(49152)=1 then print "interrupt occurred!": poke 53280,2 : poke 49152,0
250 goto 230