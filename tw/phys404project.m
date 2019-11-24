%% 01
clear all; 
close all;
syms m n i Mag Magb disMag z;
dbstop if error
Mag = 0;
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
%calc average and variance of 3X3
m = 3;
n = 3;
z = 50;
Magb = 0;
disMag = 0;
for i = 1:1:z
    [M, Spintot]=matrix(m,n);
    Magb = ( Spintot / (m * n) ) + Magb;
    disMag = ( Spintot / (m * n) )^2 + disMag;
end
disp(['Average magnetization of ', num2str(z), ' 3X3 matrix is '])
Magb = Magb / (z)
disp('with variance')
disMag = (disMag / z) - (Magb)^2

%calc average and variance of 10X10
m = 10;
n = 10;
z = 50;
Magb = 0;
disMag = 0;
for i = 1:1:z
    [M, Spintot]=matrix(m,n);
    Magb = ( Spintot / (m * n) ) + Magb;
    disMag = ( Spintot / (m * n) )^2 + disMag;
end
disp(['Average magnetization of ', num2str(z), ' 10X10 matrix is '])
Magb = Magb / (z)
disp('with variance')
disMag = (disMag / z) - (Magb)^2

%calc average and variance of 64X64
m = 64;
n = 64;
z = 50;
Magb = 0;
disMag = 0;
for i = 1:1:z
    [M, Spintot]=matrix(m,n);
    Magb = ( Spintot / (m * n) ) + Magb;
    disMag = ( Spintot / (m * n) )^2 + disMag;
end
disp(['Average magnetization of ', num2str(z), ' 64X64 matrix is '])
Magb = Magb / (z)
disp('with variance')
disMag = (disMag / z) - (Magb)^2

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