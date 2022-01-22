# sandbox `pwn` [100]

這題會讀入一段 shellcode，在 shellcode 中間插入許多的判斷。

1. 只允許執行 `sys_exit` (60) 的 syscall

2. 禁止執行 `call reg` 形式的 instruction

3. 最後加上 `epilogue` ，執行 `sys_exit`

   ```assembly
      0:   48 c7 c0 3c 00 00 00    mov    rax, 0x3c
      7:   0f 05                   syscall
   ```

在 shellcode 前面先將 registers 設置好，由於 `mmap` 有指定 address，`stack` 和 `new_code_buf` 皆是固定的，可以直接放置 `/bin/sh\0` ，並取得字串位置；
再透過 `jmp rel8` 的 instruction 跳到 `epilogue` 的 `syscall` ，即可執行 `syscall(0x3B, '/bin/sh\0', 0, 0)`  拿到 shell。

reference: [JMP — Jump (felixcloutier.com)](https://www.felixcloutier.com/x86/jmp)

# fullchain `pwn` [150]

這題有設置 seccomp rule，不能執行 `sys_exceve`，需要透過 ORW (open, read, write) 取得 flag。

有三種操作，可以選擇傳入 `local` 或是 `global` 的 `pointer`。

1. set：在 `pointer` 位置寫入 `len` 個 int，`len` <= 0x10。
2. read：讀取最多 24 個 char 到 `pointer` 位置。
3. write：使用 `printf` 輸出 `pointer` 位置的字串，有 FSB (format string bug)。

一開始 `cnt = 3`，只能執行三次操作。

1. 先利用 FSB leak `rsp`
2. 再將 `(int)&cnt+2` 放到 `stack` 上
3. 最後利用 FSB 將 `cnt` 寫成 `0x50000`

接下來可以進行無限次的操作。

- 利用 FSB leak `code base`
- 將 `printf@got` 放到 `stack` 上
- 利用 FSB leak `libc base`
- 利用 FSB 將 `printf@got` 寫成 `scanf`

將 `printf` 寫成 `scanf` 後，即可寫入不限長度的 payload。

- 在 bss 段找一塊位置放 shellcode，透過 ORW 取得 flag。
- 利用 pwntools 建立 ROP chain
  - 透過 mprotect 讓 bss 變成 RWX
  - 再跳到 shellcode
- 再將 `exit@got` 寫成 `pop rdi; ret` 的 ROP gadget
  - 因為 `call exit` 會在 `stack` 上放 return address 需要將它 pop 掉

最後輸入 ROP chain 上相同 offset 的內容，即可 `call exit` 執行 ROP chain，拿到 flag。

# fullchain-nerf `pwn` [100]

與 `fullchain` 相同，沒有 set 操作，沒有 canary，輸入及陣列大小不一樣。

使用與 `fullchain` 相同的方法，修改 io 及部分 offset 即可。

> 這兩題 source code 在 chal function 中的變數宣告順序相同，
> 但在 binary 上的排列方式因為有無 canary 而不同。
