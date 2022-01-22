# FILE note `Pwn` [300]

這題和 lab 類似，有三種操作。

1. `create`: 建立 tmp 檔案，並透過 fdopen 建立 FILE structure (`fp`)。
2. `write`: 在  `node_buf` (heap 上) 寫入任意長度的字串，存在 heap overflow 漏洞。
3. `save`: 將 `node_buf ` 透過 `fwrite` 寫到 `fp` 。

## Leak Libc Base

先建立 FILE structure，再透過 heap overflow 將 `fp` 的 fd 寫成 1 (`stdout`)。
由於此時無法知道任何合法的 address，將 `_IO_FILE` 中的 buffer 位置都寫成 0，再透過 `save` 將 buffer 修復成合法的 address。
在 buffer 位置都是 0 的情況下，`todo == n`、`do_write == todo`，會進入`_IO_new_file_overflow` ，在 【1】 `_IO_doallocbuf` 重新建立 buffer 位置。

再透過 heap overflow partial overwrite write_base，並 flags 設成 `_IO_CURRENTLY_PUTTING | _IO_IS_APPENDING` 。
被重新建立的 write_base 相對 heap base 的 offset 會是 0x690，將最後 1 bytes 寫成 \0，offset 會變成 0x600，其中 offset 0x680 是存放在 `_IO_FILE_plus` 結構的 vtable（ `_IO_wfile_jumps`）是 libc address。
進入到 `_IO_new_file_overflow` 後，

- flags 有設定 `_IO_CURRENTLY_PUTTING` ，不會經過【1】重新配置 buffer 位置。
- flags 有設定 `_IO_IS_APPENDING` ，不會經過【2】seek 失敗 return。
- 最終會進入到 【3】將 `write_base` 到 `write_ptr` 的內容印出來。

印出的範圍是 offset 0x600 ~ 0x890，會印出 vtable address，成功 leak libc address。

```c
* fwrite -> _IO_fwrite
    if (request == 0)
        return
    * _IO_sputn -> _IO_new_file_xsputn
    	...
    	if (todo + must_flush)
            ...
            do_write = todo - ...
            if (do_write)
                * _IO_OVERFLOW -> _IO_new_file_overflow (f, ch = EOF)
                	if (flags & _IO_NO_WRITES(0x0008))
                        ...
                	if (!(flags & _IO_CURRENTLY_PUTTING(0x0800)) || write_base == NULL)
                        if (write_base == NULL)
                            * _IO_doallocbuf  // --- 【1】
					if (ch == EOF)
						* return _IO_do_write (f,
								data = write_base,
								todo = write_ptr - write_base
						)
                        	* new_do_write
                                if (flags & _IO_IS_APPENDING(0x1000))
                                    offset = _IO_pos_BAD
                                else if (read_end != write_base)
                                    new_pos = _IO_SYSSEEK (...); // --- 【2】
                                    if (new_pos == _IO_pos_BAD)
                                        return 0
                                    offset = new_pos
                                * _IO_SYSWRITE -> _IO_new_file_write // --- 【3】
                                ...
                ...
			...
		...
```

## Overwrite _IO_file_setbuf to one_gadget

有 libc base 後，將 one_gadget 寫到 `_IO_file_jumps` 上。

one_gadget 需要滿足特定的 constraints 才能使用，此 libc 有以下 3 個 one_gadget，條件如下。

```sh
$ one_gadget filenote_release/libc.so.6
0xe6c7e execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL
  [r12] == NULL || r12 == NULL

0xe6c81 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL

0xe6c84 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
```

在 `exit` 時會觸發 `_IO_cleanup` 這個 function，裡面會走過 `_IO_list_all` 裡面所有的 fp，其中呼叫 `_IO_SETBUF` 的參數恰好符合 `rsi = rdx = NULL`，可以使用 0xe6c84 的 one_gadget。

```c
exit(0)
text_set_element(__libc_atexit, _IO_cleanup)
* _IO_cleanup
    * _IO_unbuffer_all
    	...
    	for(...) {
            ...
    		if (!(fp->_flags & _IO_UNBUFFERED))
                ...
    			_IO_SETBUF(fp, NULL, 0) // -> one_gadget with rsi = rdx = 0
                ...
			...
		}
		...
```

將要寫入的範圍（`_IO_file_jumps` 的 `setbuf` 位置）透過 heap overwrite 填到 write_ptr 和 write_end，並將 flags 設成 0。
再透過 `fwrite` 寫入 one_gadget，xsputn 會先將 buffer 位置填滿，因為 `write_base == NULL` 會重新配置 buffer，剩餘的內容會被寫入新的 buffer，順利將 one_gadget 寫到 vtable 上。


```c
* fwrite -> _IO_fwrite
    if (request == 0)
        return
    * _IO_sputn -> _IO_new_file_xsputn
    	...
        if (（flags & _IO_LINE_BUF) && (flags & _IO_CURRENTLY_PUTTING))
            ...
        else if (f->_IO_write_end > f->_IO_write_ptr)
            count = f->_IO_write_end - f->_IO_write_ptr; /* Space available. */
		if (count > 0)
			if (count > to_do)
				count = to_do
				write_ptr = __mempcpy (write_ptr, s, count); // --- 【1】
				...
    	if (todo + must_flush)
            ...
            do_write = todo - ...
            if (do_write)
                * _IO_OVERFLOW -> _IO_new_file_overflow (f, ch = EOF)
                	if (flags & _IO_NO_WRITES(0x0008))
                        ...
                	if (!(flags & _IO_CURRENTLY_PUTTING(0x0800)) || write_base == NULL)
                        if (write_base == NULL)
                            * _IO_doallocbuf  // --- 【2】
		...
```

最後再輸入 4 呼叫 `exit(0)`，觸發 one_gadget 取得 shell。

flag: `FLAG{f1l3n073_15_b3773r_7h4n_h34pn073}`
