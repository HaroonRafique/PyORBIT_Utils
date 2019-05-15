%% Plot LatticeFunctions & Dispersion

%% Read Dispersion File
% Initialize variables.
filename = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELIntegration/16DecDistn/LatticeFunctions/Dispersion.dat';
formatSpec = '%14f%14f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'EmptyValue' ,NaN, 'ReturnOnError', false);
fclose(fileID);

% Allocate imported array to column variable names
S_D = dataArray{:, 1};
D_x = dataArray{:, 2};
D_y = dataArray{:, 3};

clearvars filename formatSpec fileID dataArray ans;

%% Read LatticeFunctions file

% Initialize variables.
filename = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELIntegration/16DecDistn/LatticeFunctions/LatticeFunctions.dat';
formatSpec = '%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%30f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'EmptyValue' ,NaN, 'ReturnOnError', false);
fclose(fileID);

% Allocate imported array to column variable names
S = dataArray{:, 1};
x = dataArray{:, 2};
% xp = dataArray{:, 3};
y = dataArray{:, 4};
% yp = dataArray{:, 5};
% mu_x_frac = dataArray{:, 6};
% mu_y_frac = dataArray{:, 7};
Beta_x = dataArray{:, 8};
% Alpha_x = dataArray{:, 9};
Beta_y = dataArray{:, 10};
% Alpha_y = dataArray{:, 11};
D_x_EF = dataArray{:, 12};      % D_x * Energy scaling factor
% D_xp_EF = dataArray{:, 13};      
D_y_EF = dataArray{:, 14};      % D_y * Energy scaling factor
% D_yp_EF = dataArray{:, 15};
EF = dataArray{:, 16};          % Energy scaling factor

% Perform operations

D_x_lf = D_x_EF / EF;
D_y_lf = D_y_EF / EF;
% D_xp = D_xp_EF / EF;
% D_yp = D_yp_EF / EF;

% Alpha_x = -1 .* Alpha_x;
% Alpha_y = -1 .* Alpha_y;


clearvars filename formatSpec fileID dataArray ans;

%% SUBPLOTS
figure;

% Whole LHC
% xmin = 0;
% xmax = 26659;
% betamin = 1E5;
% betamax =  0;
% dmin = -4;
% dmax = 4;
% comin = -5E-2;
% comax = 5E-2;

% HEL Zoom
xmin = 9900;
xmax = 10000;
betamin = 150;
betamax = 400;
dmin = -0.5;
dmax = 0.5;
comin = -1E-2;
comax = 1E-2;


%% Beta plot
subplot(3,1,1);
title('Beta Functions');

%% Plot Betas
% beta_plots = semilogy(S, Beta_x, 'blue', S, Beta_y, 'red');
beta_plots = plot(S, Beta_x, 'blue', S, Beta_y, 'red');
hold on;
beta_legend = legend(beta_plots(),'Beta_x','Beta_y');
hold on;
set(beta_legend,'color','none');
axis([xmin,xmax,betamin,betamax]);
xlabel('s [m]');
ylabel('Beta [m]');

% Lines for HELs and IP4
line([9908.405 9908.405],[-1E5 1E5], 'color', 'c')
line([9967.005 9967.005],[-1E5 1E5], 'color', 'm')
line([9997.005 9997.005],[-1E5 1E5], 'color', 'black')

hold off;

%% Dispersion Plot
subplot(3,1,2);
title('Dispersion');

%% Plot Dispersion
Disp_plots = plot(S_D, D_x, 'blue', S_D, D_y, 'red');
hold on;
disp_legend = legend(Disp_plots(),'D_x','D_y');
hold on;
set(disp_legend,'color','none');
axis([xmin, xmax, dmin, dmax]);
xlabel('s [m]');
ylabel('D [m]');

% Lines for HELs and IP4
line([9908.405 9908.405],[-1E5 1E5], 'color', 'c')
line([9967.005 9967.005],[-1E5 1E5], 'color', 'm')
line([9997.005 9997.005],[-1E5 1E5], 'color', 'black')

hold off;

%% Closed Orbit Plot
subplot(3,1,3);
title('Closed Orbit');

%% Plot Closed Orbit
co_plots = plot(S, x, 'blue', S, y, 'red');
hold on;
co_legend = legend(co_plots(),'x','y');
hold on;
set(co_legend,'color','none');
axis([xmin, xmax, comin, comax]);
xlabel('s [m]');
ylabel('diplacement [m]');

% Lines for HELs and IP4
line([9908.405 9908.405],[-1E5 1E5], 'color', 'c')
line([9967.005 9967.005],[-1E5 1E5], 'color', 'm')
line([9997.005 9997.005],[-1E5 1E5], 'color', 'black')

hold off;

%% Clean up
clear all;
