(*Problem 5*)

fun Square(x:real)=x*x;
fun Cube(x:real)=x*x*x;
fun tab(a:real,d:real,n:real,i:real,F)=
if i>n+1.0 then []
else [(a,F(a))]@tab(a+(d),d,n,i+1.0,F);

fun tabulate(a, d, n, F)= tab(a,d,Real.fromInt(n),1.0,F);

tabulate(0.1, 2.0, 2, Square);
tabulate(1.0, ~2.0, 4, Square);
tabulate(0.1,2.0,2,Cube);