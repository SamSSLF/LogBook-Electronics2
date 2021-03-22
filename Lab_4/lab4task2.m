% Lab 4 - Task 2: 3D display of roll and pitch angles
clear all
close('all')
ports = serialportlist;
pb = PyBench(ports(end));  % create a PyBench object
model = IMU_3D();  % create the IMU 3D visualisation object
N = 50;
tic;
gx = 0; gy = 0; 	% initialise gyro angles
fig1 = figure(1);
while true
    for i = 1:N
        [p, r] = pb.get_accel();
        [x, y, z] = pb.get_gyro();
        dt = toc;
        tic;
        pitch = p*180/pi;
        roll = r*180/pi;
        gx = max(min(gx+x*dt,pi/2),-pi/2);
        gy = max(min(gy+y*dt,pi/2),-pi/2);
        clf(fig1);
        subplot(2,1,1);
        model.draw(fig1, p, r, 'Accelerometer');
        subplot(2,1,2);
        model.draw(fig1, gy, gx, 'Gyroscope');
        pause(0.1);
    end  % for
end  % while