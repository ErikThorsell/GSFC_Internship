clc, clf, clear figure, clear all

az_slew = csvread('/home/erik/Programming/git/GSFC_Internship/azel/data/hb_az.dat');
el_slew = csvread('/home/erik/Programming/git/GSFC_Internship/azel/data/hb_el.dat');

az_time_theoretical = az_slew(:,1);
az_time_real = az_slew(:,2);
az_distance = az_slew(:,3);

el_time_theoretical = el_slew(:,1);
el_time_real = el_slew(:,2);
el_distance = el_slew(:,3);

x = linspace(0, 50, 1000);
z = ones(1,1000)*90;
y = ones(1,1000)*180;

subplot(2,1,1)
hold on
plot(az_distance, az_time_real, '.')
plot(az_distance, az_time_theoretical, 'r.')
plot(y,x,'k')
plot(z,x,'k')
grid on
ylabel('Time (seconds)')
xlabel('Distance (degrees)')

legend('Real times', 'Theoretical times', 'Location', 'NorthWest')
title('Ishioka Azimuth')

subplot(2,1,2)
hold on
plot(el_distance, el_time_real, '.')
plot(el_distance, el_time_theoretical, 'r.')
grid on
ylabel('Time (seconds)')
xlabel('Distance (degrees)')

legend('Real times', 'Theoretical times', 'Location', 'NorthWest')
title('Ishioka Elevation')