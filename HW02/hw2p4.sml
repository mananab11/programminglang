(*Problem 4*)
(*Part A*)

fun take1(L) =
if L = nil then nil
else hd(L)::skip1(tl(L))

and
skip1(L) =
if L=nil then nil
else skip2(tl(L))

and 
skip2(L) =
if L = nil then nil
else skip3(tl(L))
and
skip3(L) =
if L=nil then nil
else take1(tl(L));



take1([1,2,3,4,5,6,7,8,9,10]);
skip1([1,2,3,4,5,6,7,8,9,10]);
skip2([1,2,3,4,5,6,7,8,9,10]);
skip3([1,2,3,4,5,6,7,8,9,10]);

take1([1,2]);
skip1([1,2]);
skip2([1,2]);
skip3([1,2]);

take1([]);
skip1([]);
skip2([]);
skip3([]);
