clc, clear all

files = dir('/home/erik/Programming/git/GSFC_Internship/azel/data/*.dat');

offset = 3;
kold = 0;
for file = files'
    path = sprintf('/home/erik/Programming/git/GSFC_Internship/azel/data/%s', file.name);
    csv = load(path);
    td = csv(:,2);
    td_tmp = [];
    td_sorted = [];
    yd = csv(:,3);
    yd_tmp = [];
    yd_sorted = [];
    A = [ones(size(td)) td];
    x = A\yd;
    k = x(1);
    m = x(2);
    if file.name == 'is_az.dat'
        k
        m
    end    
    while(abs(k-kold) > 1e-10)
        for i=1:size(td)
            if k*yd(i) + (m-offset) < td(i) < k*yd(i) + (m+offset)
                td_sorted = [td_sorted, td(i)];
                yd_sorted = [yd_sorted, yd(i)];
            end
        end
        % Problem: *_sorted are empty after the loop..........
        td_new = td_sorted;
        yd_new = yd_sorted;
        
        A = [ones(size(td_new)) td_new];
        x = A\yd_new;
        k = x(1);
        m = x(2);
        td_tmp = td_sorted;
        yd_tmp = yd_sorted;
        kold = k;
        td_sorted = [];
        yd_sorted = [];
    end
    if file.name == 'is_az.dat'
        k
        m
    end
    
end