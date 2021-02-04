function [Y] = plot_spec_dB(sig, fs)

% Function to plot frequency spectrum of sig
%   usage: 
%           plot_spectrum(sig, 8192)
%
% author: Peter YK Cheung
% Last mod: 24 Jan 2021
    magnitude = abs(fft(sig));
    N = length(sig);
    df = fs/N; 
    f = 0:df:fs/2;
    m_max = max(magnitude);
    Y = 20*log10(magnitude(1:length(f))/m_max); % convert Hertz to decibels
    plot(f, Y)
       axis([0 fs/2 -60 0]); % specify axis limits as a vector of four elements [xmin xmax ymin ymax]
    xlabel('\fontsize{14}frequency (Hz)')
    ylabel('\fontsize{14}Magnitude (dB)');
    title('\fontsize{16}Spectrum in dB');
  