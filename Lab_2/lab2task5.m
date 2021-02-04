clear all;
[sig fs] = audioread('two_drums.wav');
sound(sig,fs)

% plot the signal
figure(1);
clf;
plot(sig);
xlabel('Sample no');
ylabel('Signal (V)');
title('Two Drums');