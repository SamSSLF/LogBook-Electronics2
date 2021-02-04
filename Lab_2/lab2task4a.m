clear all;
ports = serialportlist;
pb = PyBench(ports(end));

% set sampling frequency
fs = 8000;
pb = pb.set_samp_freq(fs);

% Capture N samples
N = 1000;
samples = pb.get_mic(N);
data = samples - mean(samples); % remove DC offset

% plot data
figure(1);
clf
plot(data);
xlabel('Sample no');
ylabel('Signal Voltage (V)');
title('Microphone signal');

% find the spectrum;
figure(2);
plot_spec_dB(data, fs)

% create a hamming window
window = hamming(length(data));
while true
    samples = pb.get_mic(N);
    data = samples - mean(samples);
    clf;
    plot_spec_dB(data,fs);
    hold on
    plot_spec_dB(data.*window,fs);
end