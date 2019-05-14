%% Script to plot apertures and particle tracks

%% Import Transport Tracking data
tdir = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/SymplecticLossMap/NoCollTest/';
tfile = 'Transport_tracking_gamma.txt';
tfilename = strcat(tdir,tfile);
delimiter = ' ';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%[^\n\r]';
tfileID = fopen(tfilename,'r');
dataArray = textscan(tfileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(tfileID);
t_id = dataArray{:, 1};
t_turn = dataArray{:, 2};
t_s = dataArray{:, 3};
t_x = dataArray{:, 4};
t_xp = dataArray{:, 5};
t_y = dataArray{:, 6};
t_yp = dataArray{:, 7};
t_dp = dataArray{:, 8};
t_type = dataArray{:, 9};
clearvars tfilename delimiter startRow formatSpec tfileID tfile tdir dataArray ans;

%% Import Symplectic Tracking data
tdir = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/SymplecticLossMap/NoCollTest/';
tfile = 'Symplectic_tracking_gamma.txt';
tfilename = strcat(tdir,tfile);
delimiter = ' ';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%[^\n\r]';
tfileID = fopen(tfilename,'r');
dataArray = textscan(tfileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(tfileID);
s_id = dataArray{:, 1};
s_turn = dataArray{:, 2};
s_s = dataArray{:, 3};
s_x = dataArray{:, 4};
s_xp = dataArray{:, 5};
s_y = dataArray{:, 6};
s_yp = dataArray{:, 7};
s_dp = dataArray{:, 8};
s_type = dataArray{:, 9};
clearvars tfilename delimiter startRow formatSpec tfileID tfile tdir dataArray ans;

%% Import ApertureSurvey
apdirname = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/SymplecticLossMap/NoCollTest/';
apfile = 'Aperture_Survey_0.1_steps_OR_0_points.txt';
apfilename = strcat(apdirname,apfile);
delimiter = '\t';
startRow = 2;
formatSpec = '%s%s%f%f%f%f%f%f%[^\n\r]';
apfileID = fopen(apfilename,'r');
dataArray = textscan(apfileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(apfileID);
ap_name = dataArray{:, 1};
ap_type = dataArray{:, 2};
ap_s = dataArray{:, 3};
ap_length1 = dataArray{:, 4};
ap_px = dataArray{:, 5};
ap_mx = dataArray{:, 6};
ap_py = dataArray{:, 7};
ap_my = dataArray{:, 8};
clearvars apfilename delimiter startRow formatSpec apfileID dataArray ans apdirname apfile;

%% SUBPLOTS
figure;
subplot(2,1,1);
%% HORIZONTAL
%% Plot apertures
% plot positive and negative apertures (assuming symmetric)
plot(ap_s, ap_px, 'Color', 'black'), hold on;
plot(ap_s, -ap_mx,'Color', 'black' ), hold on;


%% sort and plot symplectic tracking data
sAll=[s_id,s_x/1E3,s_y/1E3,s_s,s_turn];

% sort the array
sAll_sorted=sortrows(sAll,1);

% not sure what is going on here? remove all zeros?
sfff=[0;find(diff(sAll_sorted(:,1))~=0)];
sfff=[0;sfff];

szz=sAll_sorted(:,4);
scc=sAll_sorted(:,2);

for i=1:length(sfff)-1
   plot(szz(sfff(i)+1:sfff(i+1)),scc(sfff(i)+1:sfff(i+1)),'Color','Green');
   hold on;
end

%% sort and plot transport tracking data
All=[t_id,t_x/1E3,t_y/1E3,t_s,t_turn];

% sort the array
All_sorted=sortrows(All,1);

% not sure what is going on here? remove all zeros?
fff=[0;find(diff(All_sorted(:,1))~=0)];
fff=[0;fff];

zz=All_sorted(:,4);
cc=All_sorted(:,2);

for i=1:length(fff)-1
   plot(zz(fff(i)+1:fff(i+1)),cc(fff(i)+1:fff(i+1)),'Color','red');
   hold on;
end

hold off

%% HORIZONTAL plot settings
hold on
% Set plot axis limits
%axis([19780,26659,-0.03,0.03])
%axis([19780,20400,-0.02,0.02])
axis([23100,23600,-0.03,0.03]);
title('SYMPLECTIC vs TRANSPORT: Horizontal');
xlabel('s [m]');
ylabel('y [m]');
clearvars sAll, sAll_sorted, szz, scc, All, All_sorted, zz, cc, fff, sfff;

%% VERTICAL Plot
subplot(2,1,2);
title('Vertical');
%% Plot apertures
% plot positive and negative apertures (assuming symmetric)
plot(ap_s, ap_py, 'Color', 'black'), hold on;
plot(ap_s, -ap_my,'Color', 'black' ), hold on;

%% sort and plot symplectic tracking data
sAll=[s_id,s_x/1E3,s_y/1E3,s_s,s_turn];

% sort the array
sAll_sorted=sortrows(sAll,1);

% not sure what is going on here? remove all zeros?
sfff=[0;find(diff(sAll_sorted(:,1))~=0)];
sfff=[0;sfff];

szz=sAll_sorted(:,4);
scc=sAll_sorted(:,3);

for i=1:length(sfff)-1
   plot(szz(sfff(i)+1:sfff(i+1)),scc(sfff(i)+1:sfff(i+1)),'Color','Green');
   hold on;
end


%% Transport
%% sort and plot transport tracking data
All=[t_id,t_x/1E3,t_y/1E3,t_s,t_turn];

% sort the array
All_sorted=sortrows(All,1);

% not sure what is going on here? remove all zeros?
fff=[0;find(diff(All_sorted(:,1))~=0)];
fff=[0;fff];

zz=All_sorted(:,4);
cc=All_sorted(:,3);

for i=1:length(fff)-1
   plot(zz(fff(i)+1:fff(i+1)),cc(fff(i)+1:fff(i+1)),'Color','red');
   hold on;
end

%% VERTICAL plot settings

% Set plot axis limits
%axis([19780,26659,-0.03,0.03])
%axis([19780,20400,-0.02,0.02])
axis([23100,23600,-0.03,0.03]);
title('SYMPLECTIC vs TRANSPORT: Vertical');
xlabel('s [m]');
ylabel('y [m]');

yt=0.75;
xt=0.2;
annotation('textbox', 'Position', [xt yt .10 .10],'EdgeColor','none','Fontsize',8, 'String', 'Symplectic','Color', 'g' );
annotation('textbox', 'Position', [xt yt+0.02 .10 .10],'EdgeColor','none','Fontsize',8, 'String', 'Transport', 'Color', 'r');

hold off;
clear all;