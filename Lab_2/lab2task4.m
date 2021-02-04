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

% find and plot the spectrum;
figure(2);
plot_spec_dB(data, fs)

% repeat capture and plot spectrum
while true
    samples = pb.get_mic(N);
    data = samples - mean(samples);
    figure(2)
    clf;
    plot_spec_dB(data,fs);
end