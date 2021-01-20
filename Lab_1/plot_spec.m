function plot_spec(sig,fs);
    magnitude = abs(fft(sig));
    N = length(sig);
    df =fs/N;
    f = 0:df:fs/2;
    Y = magnitude(1:length(f));
    plot(f, 2*Y/N);
    xlabel('frequency(Hz)');
    ylabel('Magnitude');
    title('Spectrum');
end