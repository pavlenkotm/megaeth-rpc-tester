+++++ +++++             Initialize counter (cell 0) = 10
[                       Loop 10 times
  > +++++ ++            Add 7 to cell 1
  > +++++ +++++         Add 10 to cell 2
  > +++                 Add 3 to cell 3
  > +                   Add 1 to cell 4
  <<<< -                Decrement counter (cell 0)
]
> ++ .                  Print 'H' (72)
> + .                   Print 'a' (97+4=101)
+++++ ++ .              Print 's' (101+7=108)
.                       Print 'h' (108)
+++ .                   Print ':' (108-46=62 err fix) use direct
> ++ .                  Print ' ' (32)
<< +++++ +++++ +++++ .  Print '0' (48)
> .                     Print 'x' (120)
