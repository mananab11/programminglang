(*Problem 2*)
(*Part A*)
fun revCycle(L)=
if List.length(L)=0 then [] else(
tl L @ [hd L]);
revCycle([2,3,4,5]);
revCycle([7,3,4,5]);
revCycle([]);
revCycle([7,3,4,~5]);

(*Part B*)
fun revCyclesHelper(L,i:int,x:int)=
if(List.length(L)=0) then [] else(
if x<=i then [] @ revCyclesHelper(tl(L) @ [hd(L)],i,x+1)
else L);

fun revCycles(L,i:int)=
revCyclesHelper(L,i:int,1);

revCycles([1,2,3,4,5,6],4);
revCycles([1,2,3,4,5,6],3);
revCycles([],5);
revCycles([1],5);
revCycles([1,2,3],0);


