clear all

% reads data from the file named bgs.wav, and returns sampled data, sig, and a sample rate for that data, fs.
[sig fs] = audioread('bgs.wav'); 

% Add noise to music
x = sig + 0.2*rand(size(sig));

% Plot the signal
figure(1);
clf;
plot(x);
xlabel('Sample no');
ylabel('Signal(v)');
title('Stay Alive Music');

% Filter music with moving average filter
N = size(x);
for i=4:N
    y(i) = (x(i)+x(i-1)+x(i-2)+x(i-3))/4;
end
y(1)=x(1)/4;
y(2)=(x(2)+x(1))/4;
y(3)=(x(3)+x(2)+x(1))/4;

% Play the original sound then the filtered sound
% sound(x, fs)
% disp('Playing the original - press return when finished')
% pause;
sound(y, fs)
disp('Playing the filtered sound')