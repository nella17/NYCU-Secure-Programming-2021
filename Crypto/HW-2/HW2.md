# Single `Crypto` [200]

此題的橢圓曲線方程式為 $y^2=x^3+ax+b$ ，給定 $p$ 及曲線上兩點，可推得 $a$ 和 $b$ 。
$$
\begin{align}
& y^2 = x^3 + ax + b \\
\Rightarrow ~ & ax + b = y^2 - x^3
\end{align}
$$

得到 $a$ 和 $b$ 後，發現 $4a^3+27b^2 = 0$，是 Singular Curve (Node)。
透過根與係數關係解出 $\alpha$ 和 $\beta$。
$$
\begin{align}
y^2 &= x^3 + ax + b \\
&= (x-\alpha)^2(x-\beta) \\
&= x^3 - (2\alpha+\beta)x^2 + (\alpha^2+2\alpha\beta)x - (\alpha^2\beta) \\
\\
&\Rightarrow
\begin{cases}
    2\alpha+\beta = 0 \\
    \alpha^2+2\alpha\beta = a \\
    -\alpha^2\beta = b \\
\end{cases}
\\
&\Rightarrow
\beta = -2\alpha
\\
&\Rightarrow
\begin{cases}
    \beta = -2\alpha \\
    2\alpha^3 = b \\
    -3\alpha^2 = a \\
\end{cases}\\
&\Rightarrow
\begin{cases}
    \alpha = \displaystyle\frac{b/2}{a/-3} \\
    \beta = -2\alpha \\
\end{cases}\\
\end{align}
$$
定義 $\phi(P(x,y))=\frac{y+\sqrt{\alpha-\beta}(x-\alpha)}{y-\sqrt{\alpha-\beta}(x-\alpha)}$，有 $\phi(P+Q)=\phi(P)\times \phi(Q)$，將橢圓曲線轉換成 DLP。

$ \phi(A) = \phi(d_A\cdot G) = \phi(G)^{d_A} $ ，透過 Pohlig-Hellman Algorithm 得到 $d_A$ 解出 FLAG。

