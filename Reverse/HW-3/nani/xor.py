from pwn import xor

exe = open('real.exe','rb').read()

code = exe[0x9af:0x9af+256]
code = xor(code, 0x87)

exe = list(exe)
exe[0x9af:0x9af+256] = code
exe = bytes(exe)
open('magic.exe','wb').write(exe)
