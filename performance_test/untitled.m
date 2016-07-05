clc, clf, clear all

% Sending files with master.f90
f_time = [ 3.4,  4, 4.6, 4.8, 4.4,  6.4,  6.8, 19.2, 113.4,     558, 1099.4];
f_bytes = [100,500,1000,2500,5000,10000,20000,40000,400000, 2000000, 4000000];
plot(f_bytes, f_time, '-')
xlabel('Bytes')
ylabel('Time [ms]')
hold on

% TC
t_time =   [1,  1,     1,   1,   1,    1,    1,    1,     2,    8.3];
t_kbytes = [100,500,1000,2500,5000,10000,20000,40000,400000,4000000];
plot(t_kbytes,t_time,'-')
hold on

% Pipes
p_time = [ 4.2,5.2,   5, 4.4,   4,  5.4,   6,  10.6,  69.8, 308, 618];
p_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000,2000000,4000000];
plot(p_kbyte,p_time,'-')
hold on

% MPI
m_time = [52.1,49.8,59,51.8,52.4,50,48.6,55.4,53,77];
m_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000,4000000];
plot(m_kbyte,m_time,'-')
%axis([0 500000 0 60])
legend('File','TCP','Pipes','MPI')