clc, clf, clear all

linewidth = 4
hold on

% Files
f_time = [ 3.4,  4, 4.6, 4.8, 4.4,  6.4,  6.8, 19.2, 113.4,     558, 1099.4];
f_bytes = [100,500,1000,2500,5000,10000,20000,40000,400000, 2000000, 4000000];
plot(f_bytes, f_time,'Color', [0/255, 205/255, 205/255],'Linewidth',linewidth)


% TCP
t_time =   [1,  1,     1,   1,   1,    1,    1,    1,     2,    8.3];
t_kbytes = [100,500,1000,2500,5000,10000,20000,40000,400000,4000000];
plot(t_kbytes,t_time,'Color', [200/255, 150/255, 0/255],'Linewidth',linewidth)

% Pipes
p_time = [ 4.2,5.2,   5, 4.4,   4,  5.4,   6,  10.6,  69.8, 308, 618];
p_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000,2000000,4000000];
plot(p_kbyte,p_time,'Color', [138/255, 10/255, 138/255],'Linewidth',linewidth)

% ZeroMQ
m_time =  [  7,  7,    7,   7,  7,    7,    7,    7,     8,   12.5,   17];
m_kbyte = [100,500,1000,2500,5000,10000,20000,40000,   4e5,     2e6,  4e6];
plot(m_kbyte,m_time,'Color', [8/255, 20/255, 200/255],'Linewidth',linewidth)

% MPI
m_time = [52.1,49.8,59,51.8,52.4,50,48.6,55.4,53,77];
m_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000,4000000];
%plot(m_kbyte,m_time,'Color',[0/255, 150/255, 69/255],'Linewidth',linewidth)


% File read only
r_time =  [  1,  1, 1.5,   2, 2.5,  3.5,  4.5,    7];
r_kbyte = [100,500,1000,2500,5000,10000,20000,40000,];
plot(r_kbyte,r_time,'Color', [255/255, 62/255, 150/255],'Linewidth',linewidth)

% Set graph properties
h_legend = legend('File','TCP','Pipes','ZeroMQ','Read only')
set(h_legend,'FontSize',35);
axis([1e3 1e4 0 10])

xlabel('Bytes', 'Fontweight','bold')
ylabel('Time [ms]', 'Fontweight','bold')
xt = get(gca, 'XTick');
set(gca, 'FontSize', 35)