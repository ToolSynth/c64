10 print "raster interrupt test"
20 poke 53280,0 : poke 53281,0 : rem ustaw kolory obramowania i tła na czarny
30 rem ładowanie handlera przerwań do adresu $c100 (49408)
40 data 169,1,141,0,192,64 : rem a9 01 8d 00 c0 40 (lda #$01 ; sta $c000 ; rti)
45 restore : rem upewnij się, że czytanie data zaczyna się od nowa
50 for i=0 to 5: read a: poke 49408+i, a: print "wrote "; a; " to address "; 49408+i: next i
60 rem ustawienie wektora irq na $c100
100 print "test complete."