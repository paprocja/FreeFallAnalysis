%%MIT License
% 
% Copyright (c) 2022 Julie Paprocki
% 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in all
% copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
% SOFTWARE. 

% This code is used to produce initial processing of the data collected 
% from the portable free-fall penetrometer bluedrop for data collected on
% exposed sediments (i.e., measurements were not collected in water). Here,
% the .bin file is read and convered to a double. The code will continually
% run until the user types "N" into the command window when prompted to
% process another drop.


%Initialize ct = 1 for coninually saving the summary output data to a master excel
%spreadsheet.
clearvars -except ct
flag = 1;

% change the following variable to the file path where you want to save the
% output data
filepath_save = 'C:\Users\jp1709\OneDrive - USNH\Documents\students\O''Brien\Data\salt marshes\9-29-23 Chapmans Landing\processed\transect 1\CL3\in water code\';
%% 

% 
while flag == 1
    %% 
    
    % clearing variables except the file path where data is saved and ct
    % for writing to a spreadsheet. Closes all old figures so the screen
    % does not get cluttered up 
    clc
    close all
    clearvars -except ct filepath_save

    % promt to input the station (this is for writing the spreadsheet)
    station = input('station', 's');  
    
    % read BlueDrop raw files; change this to match the file location where you
    % want to read the data from
    filepath = 'C:\Users\jp1709\OneDrive - USNH\Documents\blueDrop\data\Aquaculture\Aquafort 08-01-2023\';
    
    % screen prompt to input the name of the .bin file you want to read
    % (note: you only need the four digit/letter code, including any 0's,
    % and do not need to include bLog or .bin).
    filename = input('bin file name', 's');

    % Make sure to change this based on the bluedrop that was used!! (1, 2, or
    % 3) and ensure that the calibration constants are consistent with the
    % date for which data was collected
    BD = 8; %Which bluedrop are you using
    atype = 'p'; % m = mantle area, p = projected area
    tiptype = 'c'; % c = cone, p = parabolic, b = blunt
    
    % selects the mass and length of the penetrometer based on the tip
    % type. Function tipprops is located at the bottom of this script. 
    [mass,tlength] = tipprops(tiptype);
    
    % reads and opens the .bin file and converts to double.
%     file=fopen([filepath,'#',filename]);
    file = fopen([filepath, 'bLog', filename, '.bin']);
    F=fread(file,[10,120000],'bit24=>int32','b'); F=F';
    
    % sets up the excel spreadsheet
    datafile = 'data.xls';
    %% 

    %convert into SI units using the function gdata based on the blueDrop
    %number and its associated calibration constants as well as the raw
    %data
    [g2g,g18g,g50g,ppm,gX55g,gY55g,g200g,g250g] = gdata(F,BD);
    
    % plots all acclerometer data on a single plot. The user will be
    % prompted within this fuction to input the drop number of interest. 
    [filenum,start1,ent1,ploc] = alldatafig(g2g,g18g,g50g,g200g,g250g);
    
    % gets the data from the 250g accelerometer (because it will always be
    % maxed out and represent the peak deceleration)

    if max(g250g(start1:ent1))>200
        dec1=g250g(start1:ent1);%-off1;
        off2 = mean(g250g(ent1+1000:ent1+2000));
    elseif max(g200g(start1:ent1))>50
        dec1=g200g(start1:ent1);%-off1;
        off2 = mean(g200g(ent1+1000:ent1+2000));
    elseif max(g200g(start1:ent1))>18
        dec1=g50g(start1:ent1);%-off1;
        off2 = mean(g50g(ent1+100:ent1+200));
    elseif max(g200g(start1:ent1))>1.7
        dec1=g18g(start1:ent1);%-off1;
        off2 = mean(g18g(ent1+1000:ent1+2000));
    else
        dec1=g2g(start1:ent1);%-off1;
        off2 = mean(g2g(ent1+1000:ent1+2000));
    end
    dec1=dec1-off2; % Deceleration through free-fall

    pp1 = ppm(start1:ent1);
    
    % gets the data from the 2g accelerometer (because it will always be
    % maxed out)
    dec2g=g2g(start1:ent1);
%     dec3g = g18g(start1:ent1);
    
    % finds the end of the drop where acceleration = 1g.
    ent2 = findent2(dec1,ploc,start1);    
    
    % plots the 2g and 250g acceleration data 
    figure2 = figure('Color','w','units','normalized','outerposition',...
        [.125 0.4 .75 .5]);
    set(gcf,'DefaultFigureWindowStyle','docked')
    plot(dec1) 
    hold on 
    plot(dec2g)
%     plot(dec3g)
    plot(xlim,[1 1],'k') % black line representing 1 g
    scatter(ent2,dec1(ent2),'xb') % plots a x representing the end of the deployment.
    xlabel('Steps');
    ylabel('Deceleration (g)');
    grid on;
    drawnow;

    % select the start of penetration
    spike = input('Spike step?');
%     ent2 = input('end step?');

    
    % start and end of deployment.
    dec2 = dec1(spike:ent2);

    % convert from g to m/s^2
    decms=dec2*9.81;
    
    % convert from counts to time
    time = 0:1/2000:(length(decms)-1)/2000;
    
    % numeric integration using the trapezoidal rule to convert from
    % acceleration to velocity, in m/s
    v=cumtrapz(time,decms);
    vmax=max(v);
    vel=vmax-v;
    
    % numeric integration using trapezoidal rule to convert from velocity
    % to penetration depth, in m.
    dep=cumtrapz(time,vel); 
    
    % find the area based on the penetration depth, area type, and the tip
    A = areafind(tiptype,atype,dep,tlength);


    % mass of the penetrometer (in kg) x deceleration (in g) x gravitational
    % constant (in m/s^2) to get force, in N
    buoy=1020*0.002473;
    Fbe = (mass*(dec2)*9.81); %In Air
%     Fbe = ((mass-buoy)*dec2*9.81); %In Water

    qdyn = ldivide(A,Fbe);  % dynamic bearing capacity [Pa]
    srcv = log10(vel/0.02);  % Velocity portion of the strain rate correction. 
    % The 0.02 represents the quasi-static constant based on the rate of CPTs.    
    srfK = [0.2 0.4 1 1.5]; %List of strain rate factors, K, to run
    srfn = {'02', '04', '1' ,'15'}; %List of names for each srfK
    clear i
    for i = 1:length(srfK)
        statement1 = ['fsr',srfn{i},'= 1 + srfK(i)*srcv;']; eval(statement1); %Strain Rate Correction
        statement2 = ['qsbc',srfn{i},'= qdyn./fsr',srfn{i},';']; eval(statement2); %Quasi-Static Bearing Capacity [Pa]
        statement3 = ['qsbc',srfn{i},'= qsbc',srfn{i},'/1000;']; eval(statement3); %QSBC [kPa]
    end

    figure;
    set(gcf,'DefaultFigureWindowStyle','docked')
    plot(qsbc1);
    hold on;
    plot(qsbc15);
    drawnow;
    
    % start and end points for plotting the qsbc. 
    start3=input('Start time stamp?');
    ent3=input('End time stamp?');

    % this represents all data from the start to the end point just
    % selected
    depr=dep(1:ent3);
    depr1=dep(start3:ent3);
    velr=vel(1:ent3);
    dec2r=dec2(1:ent3);
    pp2 = pp1(1:ent3);

    % data limited by the new start and end points selected.
    qsbc1r=qsbc1(start3:ent3);
    qsbc15r=qsbc15(start3:ent3);
    qsbc02r=qsbc02(start3:ent3);
    qsbc04r=qsbc04(start3:ent3);

    pp3 = pp2(start3:ent3);
    qdynr=qdyn(start3:ent3)./1000; % dynamic bearing capacity

    % qsbc at K = 1.25 and K = 0.3 based on the average of K = 1.0-K = 1.5
    % and K = 0.2- K = 0.4, respectively.
    qsbc_av115=(qsbc1r+qsbc15r)/2;
    qsbc_av0204=(qsbc02r+qsbc04r)/2;

    % setting some stuff up for plotting because we want to plot things in
    % reverse order
    qsbc15rev=flipud(qsbc15r);
    qsbcall115=[qsbc1r;qsbc15rev];
    qsbc01rev=flipud(qsbc04r);
    qsbcall0204=[qsbc02r;qsbc01rev];
    depr1rev=flipud(depr1);
    depall=[depr1;depr1rev];

    % generation of the final figure
    fig = genfinalfig(qsbcall115,qsbcall0204,depall,qsbc_av115,qsbc_av0204,depr,depr1,dec2r,velr,qdynr);
    print(fig,'-dpng','-r300',[filepath_save,'bLog',filename,'-',num2str(filenum)]);

    % settting some stuff up for saving
    Penetration_time=(length(dec2))*1000/2000 ;
    [Max_QSBCav0204,I2] = max(qsbc_av0204);
    depQSBC0204 = depr1(I2)*100;
    [Max_QSBCav115,I1] = max(qsbc_av115);
    depQSBC115 = depr1(I1)*100;
    Max_QSBC02 = max(qsbc02r);
    Max_QSBC04 = max(qsbc04r);
    Max_QSBC1 = max(qsbc1r);
    Max_QSBC15 = max(qsbc15r);
    Max_qdyn = max(qdynr);
    [Max_DEC,I3] = max(dec2r);
    depDEC = depr(I3)*100;
    D = abs(max(depr))*100;
    Vi = max(velr);
    
    % saving data in the .mat file in the spot of interst and under the
    % name of the delopyment file appended with the drop number within the
    % file.
    save([filepath_save, 'bLog',filename,'-',num2str(filenum), '.mat'])

    if ct == 1
        % only if the excel sheet is new, this will write the names of the
        % columns for you
        titles = [{'File Name'}, {'Drop No.'}, {'Station'}, {'Max qsbc (K = 1-1.5) [kPa]'},...
            {'Max qsbc (K = 0.2-0.4) [kPa]'},...
            {'Max qdyn'}, {'Max Penetration Depth [cm]'},...
            {'Impact Velocity [m/s]'}, {'Peak Deceleration [g]'}];
        writecell(titles,[filepath_save, 'data.xlsx'],...
            'Sheet', 1,'Range', 'A1')
    end
    
    % writes data to the spreadsheet
    writecell(cellstr(['bLog',filename, '.bin']) ,[filepath_save, 'data.xlsx'], 'Sheet', 1,'Range', ['A',num2str(ct+1)])
    writematrix(filenum ,[filepath_save, 'data.xlsx'], 'Sheet', 1,'Range', ['B',num2str(ct+1)])
    % writecell(cellstr(day_time) ,[filepath_save, 'data.xlsx'], 'Sheet', 1,'Range', ['B',num2str(ct)])
    writecell(cellstr(station) ,[filepath_save, 'data.xlsx'], 'Sheet', 1,'Range',['C',num2str(ct+1)])
    B = [Max_QSBCav115,Max_QSBCav0204 ,Max_qdyn, D, Vi, Max_DEC];
    writematrix(B ,[filepath_save, 'data.xlsx'], 'Sheet', 1,'Range', ['D',num2str(ct+1)])

    %check for another file.
    check = input('check another drop? (y/n)', 's');

    if check == 'n'
        flag = 2;
    else
        flag = 1;
    end
    ct = ct + 1;

end
%% Sub Functions

function [g2g,g18g,g50g,ppm,gX55g,gY55g,g200g,g250g] = gdata(F,BD)
    switch BD
        % make sure that the calibration constants are appopriate for the date
        % of interest.
        case 3
            % calibration factors from July 2019
            g2g=((double(F(:,3)))-38285.6)/1615800.9; %accelerometers are in g
            g18g=((double(F(:,4)))+13738)/163516.8;
            g50g=((double(F(:,5)))-238520.6)/63666;
            ppm=((double(F(:,6)))-139040.1)/20705;  % this is psi
            g200g=(((double(F(:,7)))+12142.6)/27751.9);
            gX55g=((double(F(:,8)))-90237)/65351.5;
            gY55g=((double(F(:,9)))-57464.2)/65545.5;
            g250g=((double(F(:,10)))-40420.3)/13636.9;
            g2g(end) = []; g2g = [1;g2g];
            g200g(end) = []; g200g = [1;g200g];
            g18g(end) = []; g18g = [1;g18g];
            g200g(end) = []; g200g = [1;g200g];
            ppm=ppm*6.89475729; % convert into kPa
        case 2 % calibration factors from Aug 26, 2021
            g2g=((double(F(:,3)))+37242.2)/1639250.2; %accelerometers are in g
            g18g=((double(F(:,4)))-26867.0)/160460.5;
            g50g=((double(F(:,5)))-213923.3)/64080.7;
            ppm=((double(F(:,6)))+55518.9)/18981.7;  % this is psi
            g200g=((double(F(:,7)))-171448.6)/30334.2;
            gX55g=((double(F(:,8)))-54242.6)/64767.7;
            gY55g=((double(F(:,9)))-40574.2)/66343.1;
            g250g=((double(F(:,10)))-40614.9)/13654.6;
            ppm=ppm*6.89475729; % convert into kPa
        case 1 % calibration factors from July 2020
            g2g=((double(F(:,3)))-42590.9)/1626361.1; %accelerometers are in g
            g18g=((double(F(:,4)))-44492.9)/161125.5;
            g50g=((double(F(:,5)))-171656.1)/64020.3;
            ppm=((double(F(:,6)))+31776.1)/20679.7;  % this is psi
            g200g=(((double(F(:,7)))-723404.8)/32209.7);
            gX55g=((double(F(:,8))-54881.1)/64858.6);
            gY55g=((double(F(:,9)))-28735.5)/63839.9;
            g250g=((double(F(:,10)))+13299.7)/13697.1;
            g2g(end) = []; g2g = [1;g2g];
            g200g(end) = []; g200g = [1;g200g];
            g18g(end) = []; g18g = [1;g18g];
            g200g(end) = []; g200g = [1;g200g];
            ppm=ppm*6.89475729; % convert into kPa
            
        case 8 % calibration factors from Feb 2023
            g2g=((double(F(:,3)))--48961.0)/1629804.6; %accelerometers are in g
            g18g=((double(F(:,4)))-45301.2)/160611.4;
            g50g=((double(F(:,5)))-208714.3)/63704.3;
            ppm=((double(F(:,6)))-96576.0)/19436.3;  % this is psi
            g200g=(((double(F(:,7)))-49688.7)/32695.6);
            gX55g=((double(F(:,8))-52767.2)/64099.0);
            gY55g=((double(F(:,9)))-28735.5)/63839.9;
            g250g=((double(F(:,10)))-46439.9)/13677.9;
            g2g(end) = []; g2g = [1;g2g];
            g200g(end) = []; g200g = [1;g200g];
            g18g(end) = []; g18g = [1;g18g];
            g200g(end) = []; g200g = [1;g200g];
            ppm=ppm*6.89475729; % convert into kPa
    end
end

function [filenum,start1,ent1,ploc] = alldatafig(g2g,g18g,g50g,g200g,g250g)

    figure('Color','w','units','normalized','outerposition',[.125 0.4 .75 .5]);
    plot(g2g);
    hold on;
    plot(g18g,'r');
    plot(g50g,'g');
    plot(g200g,'k');
    plot(g250g,'m');
    
    % find the peaks within the 250 g accelerometer. May need to adjust the
    % peak prominence for the data (i.e., in softer data may need a
    % different value)
    [pks,loc] = findpeaks(g250g,'MinPeakProminence',3);
    scatter(loc,pks,'vk','filled');
    L = cell(1,length(loc));
    for j = 1:numel(loc)
        L{j} = j;
    end
    text(loc,pks+1,L)
    xlabel('Steps');
    ylabel('Deceleration (g)');
    legend('2g','18g','50g','200g','250g');
    drawnow;
    % selection of the drop to analyze.
    filenum = input('Which drop to analyze?');
    ploc = loc(filenum);
    [start1,ent1] = ptpick(ploc);
    
    end

function [start1,ent1] = ptpick(ploc)
% this code basically zooms the first plot in to the drop of interest.
    if ploc <= 1500
        start1 = 1;
        ent1 = ploc + 500;
    elseif ploc > 119500
        start1 = ploc - 1500;
        ent1 = 120000;
    else
        start1 = ploc - 1500;
        ent1 = ploc + 500;
    end
end


function ent2 = findent2(dec1,ploc,start1)
% this function finds the point where the accelerometer goes to an
% acceleration of 1g, i.e., resting
    for i = (ploc-start1):length(dec1)
        if dec1(i) <= 0
            num1 = i;
            num2 = i-1;
            break
        end        
    end
    v = abs([dec1(num1) dec1(num2)] - 0);
    loc = [num1 num2];
    [~,I] = min(v);
    ent2 = loc(I);
end

function [mass,length] = tipprops(tiptype)
% selects the mass and length of the tip of interest.
    switch tiptype
        case 'c'
            mass = 7.71;
            length = 7.87;
        case 'e'
            mass = 9.15;
            length = 8.26;
        case 'b' 
            mass = 10.30;
            length = 8.57;
    end
end

function A = areafind(tiptype,atype,d,tlength)
% finds the area of the penetrometer that is in contact with the soil
    clear k
    A1 = zeros(1,length(d));
    d1 = d*100;
    r = zeros(1,length(d));
    switch tiptype
        case 'c'
           switch atype 
               case 'm'
                   for k=1:numel(d)
                       if d1(k)<tlength
                           r(k)=d1(k)*tand(30);
                           A1(k)=pi*r(k)*(sqrt((r(k)^2)+(d1(k)^2)));
                       end
                       if d1(k)>=tlength
                           r(k)=4.375;
                           A1(k)=pi*r(k)*(sqrt((r(k)^2)+(tlength^2)));
                       end
                       A1(k)=A1(k)/10000;
                   end
                   A = A1';

               case 'p'
                   for k=1:numel(d)
                       if d1(k)<tlength
                           r(k)=d1(k)*tand(30);
                           A1(k)=pi*r(k)^2;
                       end
                       if d1(k)>=tlength
                           r(k)=4.375;
                           A1(k)=pi*r(k)^2;
                       end
                       A1(k)=A1(k)/10000;
                   end
                   A = A1';        
           end
        case 'b'
            switch atype
                case 'm'
                   for k=1:numel(d)
                       if d1(k)<tlength
                           r(k)=4.375;
                           A1(k)=pi*r(k)^2 + 2*pi*r(k)*d1(k);
                       end
                       if d1(k)>=tlength
                           r(k)=4.375;
                           A1(k)=pi*r(k)^2 + 2*pi*r(k)*tlength;
                       end
                       A1(k)=A1(k)/10000;
                   end
                   A = A1';
               case 'p'
                   for k=1:numel(d)
                       A1(k) = pi*4.375^2;
                       A1(k)=A1(k)/10000;
                   end
                   A = A1'; 
            end
        case 'p'
            switch atype
                case 'm'
                   for k=1:numel(d)
                       if d1(k)<tlength
                           r(k)=sqrt(2.4184*d1(k));
                           polarfun = @(theta,r) r.*sqrt(0.745*r.^2 + 1);
                           A1(k)= integral2(polarfun,0,2*pi,0,r(k));
                       end
                       if d1(k)>=tlength
                           r(k)=4.375;
                           polarfun = @(theta,r) r.*sqrt(0.745*r.^2 + 1);
                           A1(k)= integral2(polarfun,0,2*pi,0,r(k));
                       end
                       A1(k)=A1(k)/10000;
                   end
                   A = A1';
               case 'p'
                   for k=1:numel(d)
                       if d1(k)<tlength
                           r(k)=sqrt(2.4184*d1(k));
                           A1(k)=pi*r(k)^2;
                       end
                       if d1(k)>=tlength
                           r(k)=4.375;
                           A1(k)=pi*r(k)^2;
                       end
                       A1(k)=A1(k)/10000;
                   end
                   A = A1';                 
            end
    end
end

function fig = genfinalfig(qsbcall115,qsbcall0204,depall,qsbc_av115,qsbc_av0204,depr,depr1,dec2r,velr,qdynr)
% formatting for the final figure
    fig=figure('Color','w','units','normalized','outerposition',[0 0 1 1]);
    set(gcf,'DefaultFigureWindowStyle','docked')
    subplot(1,3,1)
    b=plot(dec2r,depr*100,'LineWidth',3,'Color','k'); hold on;
    c=plot(velr,depr*100,'LineWidth',3,'Color','k','LineStyle','--');
    set(gca,'ydir','reverse')
    ylabel('Depth [cm]','FontSize',18,'FontWeight','b');
    xlabel({'Deceleration [g] // Velocity [m/s]'},'FontSize',18,'FontWeight','b');
    legend([b;c],'Deceleration','Velocity','Location','northeast');
    set(gca,'FontSize',14,'linewidth',2,'box','on');
    xlim([0 inf]); yl = ylim; grid on;
    subplot(1,3,[2,3]); hold on
    a0=fill(qsbcall115,depall*100,'b'); hold on
    set(a0,'FaceColor',[0.7 0.7 0.7],'EdgeColor',[0.7 0.7 0.7]);
    a1=fill(qsbcall0204,depall*100,'b');
    set(a1,'FaceColor',[0.7 0.7 0.7],'EdgeColor',[0.7 0.7 0.7]);
    ax1=gca;
    grid on;
    set(ax1,'FontSize',14,'linewidth',2,'box','on');
    a=plot(qsbc_av115,depr1*100,'LineWidth',3,'Color','r');
    a2=plot(qsbc_av0204,depr1*100,'LineWidth',3,'Color','b');
    a3=plot(qdynr,depr1*100,'LineWidth',3,'Color','m');
    xlabel({'QSBC [kPa]'},'FontSize',18,'FontWeight','b');
    set(gca,'ydir','reverse')
    set(gca,'ylim',yl);
    legend([a;a2;a3],'QSBC_a_v K=1.0 & 1.5','QSBC_a_v K=0.1 & 0.2','Q_d_y_n','Location','northeast');
    xlim([0 inf]);
    ylim([0 inf])
end