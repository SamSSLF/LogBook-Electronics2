
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
pb.sine();