function sig = sine_gen(amp, f, fs, T); 
    dt = 1/fs;
    t  = 0:dt:T;
    sig = amp*sin(2*pi*f*t);
end