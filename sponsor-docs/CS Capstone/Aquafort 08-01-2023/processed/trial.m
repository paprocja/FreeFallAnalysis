load("C:\Users\jp1709\OneDrive - USNH\Documents\blueDrop\data\Aquaculture\Aquafort 08-01-2023\processed\bLog07A3-1 2.mat",'dep')

fun = @root;
rd0 = 0.2;
for a = 1:length(dep)
rd = fsolve(fun,rd0);
rd=rd*100;
rd=rd';


function F=root(rd)  %trying to use 2D non-linear system
load("C:\Users\jp1709\OneDrive - USNH\Documents\blueDrop\data\Aquaculture\Aquafort 08-01-2023\processed\bLog07A3-1 2.mat",'dep', 'qdyn', 'vel')

depr1=dep;
qdynr=qdyn/1000;
Velr=vel;

 phicv=deg2rad(32);
% phicv = 32;
Q=6;
R=1;
V50=1;
Nkt=12;
c0=300;
c1=0.46;
c2=2.96;
gammap=10;   %in kN/m3
k0=0.5;
chmin=.031; 
%F = cell(8, 1);
%ct= 1;
%within loop
%rdarray(ct) = rd;

%r=1;
%rd1=zeros(55,6);
%for Q=5:10
    k = 1;   
for j=10:numel (depr1)

pm=gammap*((1+2*k0)/3)*depr1(j);
V=(Velr(j)*0.0875)/chmin;
strainterm=1/(1+(V/V50));
% pm (j);
% strainterm(j);
% V(j);
% qdynr(j);

F(k)= qdynr(j)-(((Nkt*0.5*((6*sin(phicv))/(3-sin(phicv)))*exp(Q-1/rd(j))))+strainterm*((((c0*(pm^c1)*exp(rd(j)*c2))-(Nkt*0.5*((6*sin(phicv))/(3-sin(phicv))))*exp(Q-1/rd(j))))));
%F= qdynr(j)-(((Nkt*0.5*((6*sin(phicv))/(3-sin(phicv)))*exp(Q-1/rd)))+strainterm (j)*((((c0*(pm(j)^c1)*exp(rd*c2))-(Nkt*0.5*((6*sin(phicv))/(3-sin(phicv))))*exp(Q-1/rd)))));
% k=k+1;
%ct = ct + 1;


end

%rd1(:,r)=rd(:,1)
%r=r+1;

end



