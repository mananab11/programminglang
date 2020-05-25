(*Problem 3*)
(*Part A*)

fun removeFst(x, L)=
if List.length(L)=0 then L
else (if hd(L)=x then tl(L) else [hd(L)]@removeFst(x,tl(L)));

removeFst(6,[1,3,4,3]);
removeFst(3,[1,3,4,5,3]);
removeFst(~3,[1,~3,4,5,3]);
removeFst(3,[]);

(*Part B*)
fun remove(x,L)=
if List.length(L)=0 then L
else(if hd(L)=x then tl(L) else [hd(L)]@remove(x,tl(L)));

fun removeLst(x, L)=
List.rev(remove(x,List.rev(L)));

removeLst(0,[1,3,4,3]);
removeLst(~3,[1,~3,4,5,~3]);
removeLst(~3,[]);
removeLst(3,[1,3,4,3,5]);
