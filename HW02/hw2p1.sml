(*Part A*)
fun generatePoly(n,x:int)=
if x < n+1 then [1.0]@generatePoly(n,x+1)
else [];
fun genPoly(n:int)=
	generatePoly(n,0);
genPoly(3);
genPoly(4);
genPoly(0);
genPoly(~1);




(*Part B*)
fun length(L) =
    if (L=nil) then 0
    else 1+length(tl(L));
fun power(x, 0) = 1.0
| power(x, n) = x * power(x,n-1);
fun evaluate(P,a)=
if List.length(P)=0 then 0.0
else power(a,List.length(P)-1)*(hd P)+evaluate(List.drop(P,1),a);

fun evalPoly(P,a)=
evaluate(List.rev(P),a);

evalPoly([10.0,3.0,1.0],2.0);
evalPoly([2.0,3.0,5.0],2.0);
evalPoly([0.0],2.0);
evalPoly([1.0],2.0);



(*Part C*)
fun sum(m:real,n:real)=
m+n;

fun polyaddition(M,N) = 
if List.length(M)=0 then N
else(if List.length(N)=0 then M else( (sum(hd(M),hd(N)))::polyaddition(tl M,tl N)));

fun smultiply(M,n:real) = 
if List.length(M)=0 then []
else ((hd(M)*n)::smultiply(tl M,n));


fun multPoly(M,N) =
if List.length(M)=0 then []
else(if List.length(N)=0 then [] else (polyaddition(smultiply(M,hd(N)),multPoly(0.0::M,tl(N)))))

val M=[~1.0, 1.0];
val N=[1.0, 1.0];
multPoly(M,N);
val M=[2.0,~2.0, 2.0];
val N=[1.0, 1.0];
multPoly(M,N);
val M=[];
val N=[1.0, 1.0];
multPoly(M,N);





