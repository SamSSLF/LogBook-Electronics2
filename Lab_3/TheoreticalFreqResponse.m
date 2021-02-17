D = [0.038 1.19 43 1000];
f = [0,5,20];
s = 1i*2*pi*f;
G = 1000./abs(polyval(D,s));
G_db = 20*log10(G);
display(G_db)