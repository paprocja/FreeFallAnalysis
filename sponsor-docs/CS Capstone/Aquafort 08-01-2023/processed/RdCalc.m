% 
x = dir('\*.mat'); %file path where you have all your files
rd2 = zeros(length(x),1);
 %constants
phicv=deg2rad(32);
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

for b = 1:length(x)
    load([x(b).folder, '\', x(b).name],'dep', 'qdyn', 'vel'); %loads variables
    %use the next line to check a specific file
%     load("C:\Users\jp1709\OneDrive - USNH\Documents\blueDrop\data\Aquaculture\Aquafort 08-01-2023\processed\bLog07A3-1 2.mat",'dep', 'qdyn', 'vel')
    rd1 = zeros(1, length(dep)); %variable initation
    
    %loop to find rd as a function of depth
    for a = 10:length(dep)
        depr1=dep(a);
        qdynr=qdyn(a)/1000;
        Velr=vel(a);

        pm=gammap*((1+2*k0)/3)*depr1;
        V=(Velr*0.0875)/chmin;
        strainterm=1/(1+(V/V50));
        
        syms rd
        eqn = qdynr-(((Nkt*0.5*((6*sin(phicv))/(3-sin(phicv)))*exp(Q-1/rd)))+strainterm *((((c0*(pm^c1)*exp(rd*c2))-(Nkt*0.5*((6*sin(phicv))/(3-sin(phicv))))*exp(Q-1/rd)))))==0;
        S = solve(eqn, rd);

        try
            rd1(a) = double(S);
        catch
            break;
        end
    end

    rd1 = 100*rd1';
    rd2(b) = max(rd1);
end

