%% 01
clear all; 
close all;
syms m n i Mag varMag;
dbstop if error
for i = [3,10,64]
    m = i;
    n = i;
    [M, Spintot]=matrix(m,n);
    if i <= 11
        M
    end 
    disp(['Magnetization of ', num2str(i), 'X', num2str(i), ' matrix is'])
    Mag = Spintot / (m * n)
end    
function [M,S] = matrix(x,y)
Spintot = 0;
A = rand([x,y]);
for i = 1:1:x
    for j = 1:1:y
        a = A(i,j);
        if a >= 0.5
            A(i,j) = 1;
            Spintot = Spintot + 1;
        else
            A(i,j) = -1;
            Spintot = Spintot - 1;
        end
    end        
end
M = A;
S = Spintot;
end
%%
