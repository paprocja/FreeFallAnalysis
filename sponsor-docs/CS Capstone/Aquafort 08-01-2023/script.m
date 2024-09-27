clearvars;
close all;

filename='bLog07A3';

% read BlueDrop raw files
file=fopen(strcat(filename,'.bin')); %% Do not forget to change the Excell file as well
Drop_Name='bLog07A3';
F=fread(file,[10,120000],'bit24=>int32','b');
F=F';
% OFFSET=35; %%%% If needed to change the data place

% Calibration factors
offset=[-48961	45301.2	208714.3	96576	49688.7	23374.8	52767.2	46439.9];
cf=[1629804.6	160611.4	63704.3	19436.3	32695.6	64099	64663.7	13677.9];

% Calibration factors

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%convert into SI units
% g2g(1,1)=NaN;
g2g=((double(F(:,3)))-offset(1))/cf(1); % accelerometers are in g
g18g=((double(F(:,4)))-offset(2))/cf(2);
g50g=((double(F(:,5)))-offset(3))/cf(3);
ppm=6.89476*((double(F(:,6)))-offset(4))/cf(4);  % this is kPa
g200g=((double(F(:,7)))-offset(5))/cf(5);
gX55g=((double(F(:,8)))-offset(6))/cf(6);
gY55g=((double(F(:,9)))-offset(7))/cf(7);
g250g=((double(F(:,10)))-offset(8))/cf(8);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% plot data and select drops
figure ('units','normalized','outerposition',[0 0 1 1]);
subplot(2,2,[1 2]);
plot(g2g);
hold on;
plot(g18g,'r');
plot(g50g,'g');
plot(g200g,'k');
plot(g250g,'m');
xlabel('Steps');
hold off
ylabel('Deceleration (g)');
legend('2g','18g','50g','200g','250g');
subplot(2,2,3);
plot(gX55g,'k');
hold on
plot(gY55g,'b');
xlabel('Steps');
ylabel('Deceleration (g)');
legend('X Dir','Y Dir');
subplot(2,2,4);
plot(ppm/10);
xlabel('Steps');
ylabel('Pressure (kPa)');
drawnow

% Add more data in case other data is in other files
% Basically a repeat of the above lines
a='y';

while a=='y' || a == 'Y'
    a=input('Do you want to stitch another data file to this (y/n)?  ','s');
    if a == 'y' || a == 'Y'
        an = input('Specify name of file (only four numbers at end of filename):  ','s');
        file=fopen(strcat(num2str(an),'.bin')); %% Do not forget to change the Excell file as well
        F=fread(file,[10,120000],'bit24=>int32','b');             
        F=F';
        g2g=[g2g; ((double(F(:,3)))-offset(1))/cf(1)]; % accelerometers are in g
g18g=[g18g; ((double(F(:,4)))-offset(2))/cf(2)];
g50g=[g50g; ((double(F(:,5)))-offset(3))/cf(3)];
ppm=[ppm; 6.89476*((double(F(:,6)))-offset(4))/cf(4)];  % this is kPa
g200g=[g200g; ((double(F(:,7)))-offset(5))/cf(5)];
gX55g=[gX55g; ((double(F(:,8)))-offset(6))/cf(6)];
gY55g=[gY55g; ((double(F(:,9)))-offset(7))/cf(7)];
g250g=[g250g; ((double(F(:,10)))-offset(8))/cf(8)];

        close
        figure;
subplot(2,1,1);
plot(g2g);
hold on;
plot(g18g,'r');
plot(g50g,'g');
plot(g200g,'k');
plot(g250g,'m');
xlabel('Steps');
ylabel('Deceleration (g)');
legend('2g','18g','50g','200g','250g');
subplot(2,1,2);
plot(ppm);
xlabel('Steps');
ylabel('Hydrostatic pressure (kPa)');

    end
end
drawnow

%pause;


figure
hold on
plot(g2g)
drawnow

% pause;
datacursormode on

% off1=max(g2g)-1.7; %input('Offset? ');

start=input('Start time stamp for free-fall? ');

figure
hold on
if max(g250g(start:start+40000))>200;
    plot(g250g)
elseif max(g200g(start:start+40000))>50;
    plot(g200g)
elseif max(g200g(start:start+40000))>18;
    plot(g50g)
elseif max(g200g(start:start+40000))>1.7;
    plot(g18g)
else
    plot(g2g)
end;

% pause;
datacursormode on
drawnow


ent=input('End time stamp for penetration? ');
entp=input('End time stamp for the pressure profile? ');

if max(g250g(start:ent))>200;
    dec1=g250g(start:ent);%-off1;
    off2 = mean(g250g(ent+1000:ent+2000));
elseif max(g200g(start:ent))>50;
    dec1=g200g(start:ent);%-off1;
    off2 = mean(g200g(ent+1000:ent+2000));
elseif max(g200g(start:ent))>18;
    dec1=g50g(start:ent);%-off1;
    off2 = mean(g50g(ent+1000:ent+2000));
elseif max(g200g(start:ent))>1.7;
    dec1=g18g(start:ent);%-off1;
    off2 = mean(g18g(ent+1000:ent+2000));
else
    dec1=g2g(start:ent);%-off1;
    off2 = mean(g2g(ent+1000:ent+2000));
end;
dec1=dec1-off2; % Deceleration through free-fall
pp1=ppm(start:ent);


decX=gX55g(start:ent);
decY=gY55g(start:ent);

fig=figure ('units','normalized','outerposition',[0 0 1 1]);

subplot(2,2,[1 2]);
plot(dec1);
xlabel('Steps');
ylabel('Deceleration (g)');
hold on
xlabel('Steps');
ylabel('Deceleration (g)');
subplot(2,2,3);
plot (decX)
hold on
plot (decY)
xlabel('Steps');
ylabel('Horizontal Acceleration (g)');
subplot(2,2,4);
plot(pp1);
xlabel('Steps');
ylabel('p (kPa)');
drawnow

% pause;

start1=input('Impact Point? ');
ent1=ent-start+1;

%%% Determining offsets
off2_X=decX(start1);
off2_Y=decY(start1);

dec2=dec1(start1:ent1)-dec1(start1); % Deceleration through penetration
%decX2=decX(start1:ent1)-off2_X;
%decY2=decY(start1:ent1)-off2_Y;
decX2=decX(start1:ent1);
decY2=decY(start1:ent1);

weight=7.71;
    
pp2=pp1(start1:length(pp1));

t=1/2000; % measurement steps with 2kHz

a=length(dec1);

for i=1:a;
    time(i)=i*t;
end;

a=length(dec2);

for i=1:a;
    time2(i)=i*t;
end;

pp3=ppm(ent:entp);
for i=1:numel(pp3);
    time3(i)=i*t;
end

%time=time/1000; % in ms
dec3=dec2*9.81;  %convert deceleration from [g] to [m/s²]

buoy=1020*0.002473;%((0.33*0.044*0.044*pi*0.08)+(0.33*0.044*0.044*0.40*pi)+(0.044*0.044*pi*0.15));
fsr=((weight)*dec3);%-buoy;    %dynamic sediment resistance force [N] with mass of BlueDrop = 8.5 kg

v=cumtrapz(time,dec1*9.80665);  %integration of deceleration to deliver velocity
vmax=max(v);
vel=vmax-v;             %changing velocity direction
vel2=vel(start1:ent1);


dep=cumtrapz(time,vel);  %calculation of depth
dep=(-1)*dep;
corr=mean(ppm(start-200:start));
corrd=corr/9.807; % Correction for depth in meters
dep=dep-corrd;
dep2=dep(start1:ent1) - dep(start1);

decX3=decX2*9.81;
decY3=decY2*9.81;

vX=cumtrapz(time2,decX3);
vY=cumtrapz(time2,decY3);

dh_X=cumtrapz(time2,vX);
dh_X1=abs(dh_X)*100;
dh_Y=cumtrapz(time2,vY);
dh_Y1=abs(dh_Y)*100;
Tilt_X_cm=max(dh_X1);
% display(Tilt_X);

Tilt_Y_cm=max(dh_Y1);
% display(Tilt_Y);

l=log10(vel2/0.02);        %quasi-static reference velocity 0.02 m/s
fac=1+l;
fac1=1+(1.5*l);

fqsr=ldivide(fac,fsr);  %quasi-static sediment resistance force [N]
fqsr1=ldivide(fac1,fsr);

d=(-1)*dep2;             %penetration depth [m]


    for k=1:numel(d)
        d1(k)=d(k)*100; % convert m to cm
        if d1(k)<7.57;
            r(k)=d1(k)*tand(30);
            A1(k)=(pi*r(k)*(sqrt((r(k)*r(k))+(d1(k)*d1(k)))));
        end;
        if d1(k)>=7.57;
            r(k)=4.375;
            A1(k)=pi*r(k)*(sqrt((r(k)*r(k))+(7.57*7.57)));
        end;
        
    end;
    
A1=A1/10000;     
A=A1';


qdyn=ldivide(A,fsr);  %dynamic bearing capacity [Pa]
qdyn=qdyn/1000;       % [kPa]
qq=ldivide(A,fqsr);   %quasi-static bearing capacity [Pa]
qq=qq/1000;
qq1=ldivide(A,fqsr1);
qq1=qq1/1000;


figure;
plot(qq);
hold on;
plot(qq1);
drawnow

% pause;

start3=input('Start time stamp? ');
ent3=input('End time stamp? ');

depr=dep2(1:ent3);
depr1=dep2(start3:ent3);
velr=vel2(1:ent3);
dec2r=dec2(1:ent3);
pp2r=pp2(1:ent3);
qqr=qq(start3:ent3);
qq1r=qq1(start3:ent3);
[Mqqr, Iqqr] = max(qqr);  %Max qsbc and its location
qav=(qqr+qq1r)/2;
qdiff=qq1r-qqr;
qdyn=qdyn(start3:ent3);     % [kPa]
fqsr=fqsr (start3:ent3);   %quasi-static sediment resistance force [N]
fqsr1=fqsr1 (start3:ent3); 
% nc=nc(start3:ent3);
fqsrav=(fqsr+fqsr1)/2;



format bank

%%%%% Output Table
% Offset_1=off1;
Start_1=start;
End_1=ent;
Offset_2=off2;
Start_2=start1;
End_2=ent1;
Start_3=start3;
End_3=ent3;
depm = dep(start1) + 0.08833; %calculate depth of water in meters
Water_depth=depm;  %%%+vmax*vmax/2/9.81; %%%%%bernoulli corrected
Max_Decceleration=max(dec2r);
Max_Decceleration_1=Max_Decceleration;
Max_Velocity=vmax;
Penetration_Depth_cm=(-dep2(end))*100;
Depth_max_qsbc_cm=(depr1(Iqqr))*-100;
Max_qsbc=max(qqr);
Max_qsbc_Av=max(qav);
Max_qsbc_Low=max(qq1r);
qq1rev=flipud(qq1r);
%qq1rev=qq1rev';
qqall=[qqr;qq1rev];
depr1rev=flipud(depr1);
depall=[depr1;depr1rev];


        onesones=ones(length(pp2r),1);
        Reference_line=pp2r(1)* onesones-depr*9.81;

FIGURE=figure('Color','w','units','normalized','outerposition',[0 0 1 1]);
hold on;
a0=fill(qqall,depall*100,'b');
a=plot(qav,depr1*100,'LineWidth',2,'Color',[0.2 0.2 0.2]);
b=plot(dec2r,depr*100,'LineWidth',2,'Color','b');
c=plot(velr,depr*100,'LineWidth',2,'Color','k','LineStyle','--');
set(a0,'FaceColor',[0.7 0.7 0.7],'EdgeColor',[0.3 0.3 0.3]);
ax1=gca;
grid on;
p_depth=depr1*100;
set(ax1,'FontSize',12,'linewidth',1,'box','on');
ylabel('Penetration Depth [cm]','FontSize',14,'FontWeight','b');
xlabel({'Deceleration [g] // Velocity [m/s]' 'QSBC [kPa]'},'FontSize',14,'FontWeight','b');
legend([b;c;a],'Deceleration','Velocity','QSBC','Position','northeast');

 
    
for i=1:numel(qav)
    if qav(i)>1
        break
    end
end

PD1 = -1*p_depth(i); % Depth at which qsbc=1kPa

clear i

for i=1:numel(p_depth)
    if p_depth(i)<-10
        break
    end
end

TS = qav(i); % Surface strength (@10cm)

out = [Max_Decceleration Penetration_Depth_cm Water_depth Max_qsbc Max_qsbc_Av Max_qsbc_Low PD1 TS vel2(1)];
xlswrite(strcat(filename,'_',num2str(start),'.xlsx'),out)


% PRESSURE CORRECTION
figure
plot(dec1*9.8063799127023900260141488920588,dep)
hold on
plot(vel,dep,'r')
p_h = -dep.*9.807;
plot(p_h,dep,'k')
dep_imp = depm;
plot([min(dec3)-20 max(p_h)+50],[dep_imp dep_imp],'--')
plot([min(dec3)-20 max(p_h)+50],[dep_imp-0.08833 dep_imp-0.08833],'k--')
plot(pp1,dep,'y')
xlabel('dec(m/s2), v(m/s), and Pressure (kPa)')
ylabel('Vertical Distance (m)')

legend('Dec (m/s2)','Velocity (m/s)','Hydrostatic Pressure','Point of impact','Point of impact + 8.833 cm','Measured Pressure')
grid on


fc=0.5; % Pressure coeffecient (1 means full stagnation)
p_b = pp1 + fc*((vel.^2)/2);% + (-smooth(dec1,200)*9.807).*(-dep);
plot(p_b,dep,'m')

legend('Dec (m/s2)','Velocity (m/s)','Hydrostatic Pressure','Point of impact','Point of impact + 8.833 cm','Measured Pressure','Bernoulli corrected pressure')
grid on
hold off


figure
plot(sqrt(time3),pp3)
hold on
plot(sqrt(time3),smooth(pp3,200),'k')
xlabel('Square-root of time (seconds)')
ylabel('Pore pressure (kPa)')
grid on