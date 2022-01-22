# HNP-revenge  `Crypto` [250]

輸入兩次不同的文字$m_1,m_2$，會得到兩組 signature $(r_1,s_1),(r_2,s_2)$，
令 $h_1, h_2$ 為文字加 salt 後經過 md5 運算後的值。

```python
h1 = sha256(m1.encode()).digest()
h1 = md5(long_to_bytes(prikey.secret_multiplier) + h1).hexdigest()
```

兩次的 k 有共同的 high bits，$K_1=\text{hK}+k_1,K_2=\text{hK}+k_2$，其中 
```python
hK = int(md5(b'secret').hexdigest() + '0'*32, 16)
```

（參考簡報）

$$
\begin{align*}
& s_1 \equiv K_1^{-1}(h_1+dr_1) \mod n \\
& s_2 \equiv K_2^{-1}(h_2+dr_2) \mod n \\
\Rightarrow ~ & K_1 - s_1^{-1}s_2r_1r_2^{-1}K_2+s_1^{-1}r_1h_2r_2^{-1} - s_1^{-1}h1 \equiv 0 \mod n \\
\end{align*}
$$

令 $t=-s_1^{-1}s_2r_1r_2^{-1},~u=s_1^{-1}r_1h_2r_2^{-1} - s_1^{-1}h1$，
$$
\begin{align*}
& K_1+tK_2+u \\
\equiv ~ & (\text{hK}+k1)+t(\text{hK}+k_2)+u & \mod n \\
\equiv ~ & k1 + tk_2 + (\text{hK}(t+1)+u) & \mod n \\
\equiv ~ & 0 & \mod n \\
\end{align*}
$$

令 $w=(\text{hK}(t+1)+u)$
建構 lattice basis
$$
L=
\begin{pmatrix}
n & 0 & 0 \\
t & 1 & 0 \\
w & 0 & K \\
\end{pmatrix} \\
\begin{align}
\exist & ~q\in\Z, s.t. \\
& (q,k_2,1)L\\
= & (qn+tk_2+w,k_2,K)\\
= & (-k_1,k_2,K)
\end{align}
$$

存在 $\textbf{\emph{v}}=(-k1,k2,K)$ 在這個 lattice 裡，
$K<(nK)^{1/3}\Rightarrow K<n^{1/2}$，計算上取 $K=16^{32}$。

在 sage 中，透過 `L.LLL()` 計算 $\textbf{\emph{v}}$。
由於 LLL 可能找不到 $\textbf{\emph{v}}$ ，需要跑多次的 exploit 才能拿到 flag。

