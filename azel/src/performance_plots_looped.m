%%
clc, clf, clear all

linewidth = 4;

% Files
f_time =  [2878,3019,3167,3544,4191, 5674, 8363,14265,114560];
f_bytes = [ 100, 500,1000,2500,5000,10000,20000,40000,400000];
%plot(f_bytes, f_time,'Color', [0/255, 205/255, 205/255],'Linewidth',linewidth)
hold on 

% TCP
t_time =  [  8, 11,  12,  14,  20,   27,   40,   74,   421];
t_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000];
plot(t_kbyte,t_time,'Color', [200/255, 150/255, 0/255],'Linewidth',linewidth)


% Pipes
p_time =  [ 27, 89, 173, 398, 851, 1600, 3086, 6398, 62230];
p_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000];
plot(p_kbyte,p_time,'Color', [138/255, 10/255, 138/255],'Linewidth',linewidth)


% ZeroMQ
z_time =  [ 35, 36,  36,  36,  40,   57,   84,   84,   437];
z_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000];
plot(z_kbyte,z_time,'Color', [8/255, 20/255, 200/255],'Linewidth',linewidth)


% MPI
m_time =  [ 66, 57,  57,  62,  64,   73,   90,  131,   722];
m_kbyte = [100,500,1000,2500,5000,10000,20000,40000,400000];
plot(m_kbyte,m_time,'Color', [0/255, 150/255, 69/255],'Linewidth',linewidth)

% Read only
r_time =  [ 12, 50,  89, 215, 425,  840, 1660, 3300];
r_kbyte = [100,500,1000,2500,5000,10000,20000,40000];
plot(r_kbyte,r_time,'Color', [255/255, 62/255, 150/255],'Linewidth',linewidth)





%plot(f_bytes, f_time, '-')
h_legend = legend('TCP','Pipes', 'ZeroMQ','MPI', 'Read only', 'Location','NorthWest');
set(h_legend,'FontSize',35)
axis([1e3 5e3 0 500])

xlabel('Bytes, looped 1000 times', 'Fontweight','bold')
ylabel('Time [ms]', 'Fontweight','bold')

xt = get(gca, 'XTick');
set(gca, 'FontSize', 35)

