clear
Tc = 2/log(1+sqrt(2));
N = 200; K = 1000; J = 1;
T = (0.5:0.1:1.5)'*Tc; %from 0.5Tc to 1.5Tc
M(size(T)) = 0;
a = ceil(rand(N,N)*1.5)*2 - 3;
for t = 1 : size(T,1)
    p = [1 1 1 exp(-4*J/T(t)) exp(-8*J/T(t))];
    s(1:K,1) = 0;
    for k = 1 : K
        r0 = ceil(rand(N^2,2)*N);rn = mod(r0 - 2,N)+1; rp= mod(r0,N)+1;
        r = rand(N^2,1);
        for n = 1 : N^2
            if (r(n) < p(((a(rn(n,1),r0(n,2))+ a(rp(n,1),r0(n,2))+ a(r0(n,1),rn(n,2))+ a(r0(n,1),rp(n,2)))*a(r0(n,1),r0(n,2))/2 +3)))
                a(r0(n,1),r0(n,2)) = -a(r0(n,1),r0(n,2));%flip
            end
        end
        s(k) = sum(sum(a))/N^2;
    end
    M(t) = sum(s(1:K))/100; %only run the last 100 of 1000 run.
    imagesc(a);
    axis equal off;
    drawnow;
    [t M(t)]
end
figure;
plot(T/Tc, abs(M),'o');
hold on;
Tf = (0.5:0.001:1)*Tc';
plot(Tf/Tc, real((1-sinh(2*J*Tf.^-1).^-4).^(1/8)));