% Lab 4 - Task 3: 3D display of effects of Complementary Filter
clear all
close('all')
ports = serialportlist;
pb = PyBench(ports(end));  % create a PyBench object
model = IMU_3D();
N = 50;
fig1 = figure(1);
gx = 0; gy = 0;             % gyro initial angles
angle_x = 0; angle_y = 0;   % combined angle using filter
alpha = 0.7; beta = 1-alpha; % weighting factor
tic
while true
    for i = 1:N
        [p, r] = pb.get_accel();
        [x, y, z] = pb.get_gyro();
        dt = toc;
        tic;
        % integration for gyro angles
        gx = max(min(gx+x*dt,pi/2),-pi/2);
        gy = max(min(gy+y*dt,pi/2),-pi/2);
        
        % complementary filtered angles
        angle_x = alpha*(angle_x + x*dt) + beta*r;
        angle_y = alpha*(angle_y + y*dt) + beta*p;
                
        figure(fig1)
        clf(fig1);
        subplot(3,1,1);
        model.draw(fig1, p, r, 'Accelerometer');
        subplot(3,1,2);
        model.draw(fig1, gy, gx, 'Gyroscope');
        subplot(3,1,3);
        model.draw(fig1, angle_y, angle_x, 'Filtered');
        pause(0.1);
    end  % for
 end  % while