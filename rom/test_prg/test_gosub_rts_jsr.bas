10 print "test 2: gosub/return"
20 gosub 100
30 print "wróciłem do linii 30"
40 gosub 100
50 print "wszystko ok - koniec testu 2"
60 end

100 print "  -> w podprogramie (linia 100)"
110 return