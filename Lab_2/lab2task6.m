clear all;
[sigG, fsG] = audioread('guitar.wav');
[sigB, fsB] = audioread('bass.wav');

sigC = sigG + sigB;

figure(1);
clf;
plot(sigC);

xlabel('Sample no');
ylabel('Signal (V)');
title('Guitar and Bass');