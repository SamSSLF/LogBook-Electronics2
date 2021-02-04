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

% Divide signal into segments and find its energy
T = 0.02;
N = fs*T;
E = [];
for i=1:N:length(sig)-N+1
    seg = sig(i:i+N-1);
    E = [E seg'*seg];
end

% plot the energy graph and the peak values
figure(2);
clf;
x = 1:length(E);
plot(x, E)
xlabel('Segment number');
ylabel('Energy');
hold on

% find the local maxima
[pks locs] = findpeaks(E);
plot(locs,pks,'o');
hold off

%plot spectrum of energy
figure(3)
plot_spec(E - mean(E), 1/T);