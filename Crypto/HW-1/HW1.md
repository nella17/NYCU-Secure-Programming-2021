# nLFSR `Crypto` [150]

`state` 和 `poly` 都可以看成長度為 $64$ 的 binary array。
以下用 $\text{st}[i]$ 表示經過 $i$ 次 `step()` 後的 `state`，$o[i+1]$ 表示第 $i+1$ 次 `step()` 的回傳值，
用 $s[i][j]$ 表示 $(\text{st}[i] >> j) \&1$，用 $p[j]$ 表示 $(\text{poly} >> j) \&1$。($i,j\in \{N,0\}$)

由於 `out = state & 1` 只有 0 和 1，可以將 `if out: state ^= poly` 改寫成 `state ^= poly * out`。

觀察 `step()` ，可列出以下轉移式。
$s[i+1][j] = s[i][j+1] \oplus (p[j] \cdot s[i][0]) ~ (i,j\in \{N,0\})$

在 `GF(2)` 下，xor 和加法相同，可推得係數靠左的 companion matrix。
定義 $M$ 和 $S_i$ 如下，$M$ 表示 $64\times64$ 的矩陣，$S_i$ 表示 $s[i][j]$ 形成的 column  vector。
若 $L$ 是一個矩陣，定義 $L[k]$ 表示 $L$ 的第 k 個 row 形成的 row vector。
$$
S_i=
M^i\cdot S_0 = 
\begin{pmatrix}
p[0] & 1 & 0 & \cdots & 0 & 0 \\
p[1] & 0 & 1 & \cdots & 0 & 0\\
\vdots  & \vdots & \vdots  & \ddots & \vdots & \vdots  \\
p[62] & 0 & 0 & \cdots & 0 & 1 \\
p[63] & 0 & 0 & \cdots & 0 & 0
\end{pmatrix}
^i
\begin{pmatrix}
s[0][0] \\ s[0][1] \\ \vdots \\ s[0][63] \\ s[0][64]
\end{pmatrix}
=
\begin{pmatrix}
s[i][0] \\ s[i][1] \\ \vdots \\ s[i][63] \\ s[i][64]
\end{pmatrix} \\
$$

因此 $o[i+1]=s[i][0]=(M^i)[0] \cdot S_0$，
第 $k$ 次 `random()` 的回傳值會是 $o[43k]=s[42k-1][0]$，
透過解 $64$ 個聯立方程式可得到 $\text{st}[0]$ ，
找出 $\text{st}[0]$ 後即可預測所有的 $o[i+1]$。

