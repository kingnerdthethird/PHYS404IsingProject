clear all;
close all;
dbstop if error

%parameters
N = 200; %size 200x200
Q = 800; % # ofstep(each step flip N^2 times) 
J = 1; %coupling const
kT = 2; 
B = 0;% +pointing up
%allow B to change
Bmin = -1; 
Bmax = 1; 
dB = 0.01;%step size
%allow T to change while fliping
Tmin = 0.5; 
Tmax = 0.5; 
dT = 0;%step size

a = ceil(rand(N,N)*2)*2 - 3;%generate +-1 matrix
                                                        
% calc energy of initial condition
   A = zeros(N+2,N+2);
   %middle
   for i = 1:1:N
    for j = 1:1:N
        A(i+1,j+1) = a(i,j);
    end
   end

   %left
   for i = 1:1:N
    A(i+1,1) = a(i,N);
   end

   %right
   for i = 1:1:N
    A(i+1,N+2) = a(i,1);
   end

   %up
   for i = 1:1:N
    A(1,i+1) = a(N,i);
   end

   %down
   for i = 1:1:N
    A(N+2,i+1) = a(1,i);
   end
   %calc E initial
   E0 = 0;
   for i = 2:1:N+1
    for j = 2:1:N+1
        E0 = ((-1)*J*A(i,j)*(A(i+1,j)+A(i-1,j)+A(i,j+1)+A(i,j-1))) + E0;
    end
   end

E = zeros(1,15*N^2);%array record change in energy
%E(1,1) = E0;%energy of initial condition
DE = (-J)*[8 4 0 -4 -8];%energy difference after and before filp
%DEd = -1*DEu;%middle down
dE = 0;%parameter for dE
dEm = 0;%parameter for dE based on B
dEt = 0;% total dE
Eend = E0;


for q = 1:Q
     %changing T
     kT = kT + dT;
     if (kT < Tmin) || (kT > Tmax)
         dT = -dT;
     end
     %changing B
     B = B + dB;
     if (B < Bmin) || (B > Bmax)
         B = -B;
     end
     
     r0 = ceil(rand(N^2,2)*N);%random position (Px,Py)
     rn = mod(r0 - 2,N)+1; %(Px-1,Py-1)
     rp= mod(r0,N)+1;%£¨Px+1,Py+1£©
     r = rand(N^2,1);%give a random number for each random position in r0 to judge flip or not
         for n = 1 : N^2
              class = ((a(rn(n,1),r0(n,2))+ a(rp(n,1),r0(n,2))+ a(r0(n,1),rn(n,2))+ a(r0(n,1),rp(n,2)))*a(r0(n,1),r0(n,2))*0.5) + 3;
              % at this random point, what is the class(output 1,2,3,4,5)
                         %dEm based on B field
                         if a(r0(n,1),r0(n,2)) > 0 %if the middle of the random chose position is +1
                                dEm = 2*B; % after flip - before flip 
                         elseif a(r0(n,1),r0(n,2)) < 0  % the middle is -1
                                dEm = -2*B;
                         end
              
              dE = DE(1, class);
              dEt = dE + dEm;
              p = [1 1 1 exp(-4*J/kT) exp(-8*J/kT)];%only works for B = 0
              
              %flip or not based on dE
              
                          %if dE <= 0
                             %a(r0(n,1),r0(n,2)) = -a(r0(n,1),r0(n,2));
                             %calc energy after this step E = E + dE
                             %E(1,n+1) = E(1,n) + 2*dE;       
                             %not flip this position
                         %else
                  if r(n) < exp(-dEt/kT) %if r(n) < p(1,class) %random number < boltzman only for B = 0  
                      a(r0(n,1),r0(n,2)) = -a(r0(n,1),r0(n,2));
                      %calc energy after this step E = E + dE
                     
                      if q <= 15
                         E(1,n+(q-1)*N^2) = 2*dEt;
                         Eend = Eend + 2*dEt;
                      end
                  end
                          %flip based on e
              %end
         
         
         end
     
     
     imagesc(a);
     axis equal off;
     drawnow;
end

%plot E-t plot
z = 600000;
x = 1:1:z;
Ez = zeros(1,z);
Ez(1,1) = E0;
for i = 2:1:z
    Ez(1,i) = E(1,i) + Ez(1,i-1);
    
end

figure;
plot(x,Ez)
axis([0,600000,-200000,1000])
title('E-t plot')

