set encoding utf8
set datafile separator ','
p "freq0.dat" using 1:2 w l,\
  "freq1.dat" using 1:2 w l
                                 
