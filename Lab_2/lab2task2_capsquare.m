clear all
ports = serialportlist;
pb = PyBench(ports(end));

% Set the various parameters
f = 440;
fs = 8000;
pb = pb.set_sig_freq(f);
pb = pb.set_samp_freq(fs);
pb = pb.set_max_v(3.0);
pb = pb.set_min_v(0.5);
pb =pb.set_duty_cycle(50);

% generate a sinusoidal signal between max_v and min_v
pb.square();

% Capture N samples
N = 1000;
samples = pb.get_block(N);
data = samples - mean(samples);

% plot data
figure(1);
plot(data(1:200),'o');
hold on
plot(data(1:200));
xlabel('Sample no');
ylabel('Signal voltage (V)');
title('Captured signal');
hold off

%find spectrum
figure(2);
plot_spec(data,fs);