%% Script to plot JawImpact, jaw half gaps from collimator_survey etc
%% Initialize variables.
filename = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/AV/10Mar16_Ap_test/jaw_impact_TCP.C6R7.B2_0.txt';
delimiter = ' ';
formatSpec = '%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
startRow = 2;
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);


ji_id = dataArray{:, 1};
ji_x = dataArray{:, 2};
ji_px = dataArray{:, 3};
ji_y = dataArray{:, 4};
ji_yp = dataArray{:, 5};
ji_ct = dataArray{:, 6};
ji_dp = dataArray{:, 7};
ji_turn = dataArray{:, 8};

clearvars filename delimiter formatSpec fileID dataArray ans;

%% Plot JawImpact
scatter(ji_x, ji_y, 1, 'filled'), hold on

%% Plot jaw half gaps

% positive gap
pgap = 0.00151633;
line([pgap pgap],[-1E-3 1E-3]), hold on
%negative gap
ngap = pgap;
line([-ngap -ngap],[-1E-3 1E-3]), hold on

%% Plot options
%minx = 1.5E-3;
%maxx = 1.57E-3;
minx = -1.57E-3;
maxx = -1.5E-3;

miny = -1E-3; 
maxy = 1E-3;
axis([minx,maxx,miny,maxy])

hold off