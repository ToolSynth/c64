10 print "test 10: dzielenie przez zero"
20 on error goto 100
30 a=10 : b=0
40 print "Wynik dzielenia: "; a/b
50 end
100 print "Błąd: dzielenie przez zero wykryte, test zaliczony."
110 end