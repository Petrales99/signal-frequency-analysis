
## Fourier Transform
The Fourier transform is a very useful mathematical tool for signal analysis; it allows us to move from studying a phenomenon from the time domain to the frequency domain.

The Fourier transform (FT) is an operation that allows you to obtain the frequency content of a signal, while the inverse Fourier transform allows you to obtain a signal from its frequency content.

Let $f(x)$ be a function defined in the interval $(-\pi,\pi)$; $f(x)$ can be developed in Fourier series if

$$ f(x)=\frac{1}{2}a_0+\sum_{n=1}^{\infty}a_ncos(nx)+b_nsin(nx) $$

where, integrating both sides between $−\pi$ and $\pi$ and taking into account the symmetries of $sin(x)$ and $cos(x)$, we have

$$a_n=\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)cos(nx)dx, \hspace{0.1 cm} b_n=\frac{1}{\pi}\int_{-\pi}^{\pi}f(x)sin(nx)dx.$$

$a_0,a_n$ and $b_n$ called Fourier coefficients.

More generally, if $f(x)$ is defined in the interval $(c−d,c+d)$ then

$$f(x)\sim \frac{a_0}{2}+\sum_{n=1}^{\infty}a_ncos(\frac{n\pi(x+c)}{d}) +b_nsin(\frac{n\pi(x+c)}{d})$$ in cui $$a_n=\frac{1}{d}\int_{c-d}^{c+d}f(x)cos(\frac{n\pi(x+c)}{d})dx, \\  b_n=\frac{1}{d}\int_{c-d}^{c+d}f(x)sin(\frac{n\pi(x+c)}{d})dx.$$

Taking into account the Euler identity ( $eix=cos(x)+i⋅sin(x)$ ) it is possible to rewrite the Fourier series as follows
$$\frac{a_0}{2}+\sum_{n=1}^{\infty}(a_ncos(nx)+b_nsin(nx))=\sum_{n=-\infty}^{+\infty}c_ne^{inx} $$
where

$$c_n =
\begin{cases}
\frac{1}{2}(a_n - i b_n) & n \geq 1 \\
\frac{a_0}{2} & n = 0 \\
\frac{1}{2}(a_{-n} - i b_{-n}) & n \leq -1
\end{cases}$$

From which, in general
$$f(x)=\sum_{-\infty}^{+\infty}c_n\frac{\pi}{L} e^{\frac{in\pi x}{L}}$$ with $$c_n=\frac{1}{2\pi}\int_{-L}^{L}e^{\frac{-in\pi x}{L}}f(x)dx.$$

At the limit for $L\to \infty$ $$f\sim \int_{-\infty}^{+\infty}\hat{f}(\omega)e^{i\omega x}d\omega$$ where $$\hat{f}(\omega)=\frac{1}{2\pi}\int_{-\infty}^{+\infty}f(x)e^{-i\omega x}dx.$$
The function $\hat{f}(x)$ is called the Fourier transform of $f(x)$.

The spectrum of a function represents the trend of the amplitudes of the Fourier coefficients as a function of frequency.