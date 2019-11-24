%%
clear all; 
close all;
syms n i j Spintot;
n = 10;
Spintot = 0;
A = rand(n);
for i = 1:1:n
    for j = 1:1:n
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
A
Spintot
%%