10 print "c64 keyboard test - press 'q' to exit"
20 print "press keys and see them displayed below..."
30 print : print "key pressed: ";

40 rem --- pętla testująca klawiaturę ---
50 get a$
60 if a$="" then goto 50  : rem jeśli nie naciśnięto klawisza, pętla się powtarza
70 print a$; : rem wyświetlenie naciśniętego klawisza
80 if a$="q" then print : print "exiting...": end  : rem jeśli "q", koniec
90 goto 50  : rem powrót do sprawdzania klawiatury