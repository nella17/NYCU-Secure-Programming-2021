b close
set follow-fork-mode child
r
c
fin
ni 12
dump memory shellcode $rax $rax+216
x/s $rdi
q
