%% Script to plot ApertureTest

%% Import Aperture File
% filename = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Thesis/data/AV/Aperture_6p5TeV_beam2.tfs';
% delimiter = ' ';
% formatSpec = '%q%q%q%f%f%f%f%f%f%[^\n\r]';
% fileID = fopen(filename,'r');
% dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'EmptyValue' ,NaN, 'ReturnOnError', false);
% fclose(fileID);
% 
% m_el = dataArray{:, 1};
% m_name = dataArray{:, 2};
% m_type = dataArray{:, 3};
% m_s = dataArray{:, 4};
% m_L = dataArray{:, 5};
% m_ap1 = dataArray{:, 6};
% m_ap2 = dataArray{:, 7};
% m_ap3 = dataArray{:, 8};
% m_ap4 = dataArray{:, 9};
% clearvars filename delimiter formatSpec fileID dataArray ans;

clear all;
mydata= importdata('/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Thesis/data/HELFullBeam/HL_v1.2.1_Aperture.tfs') ;
aperture=[mydata.data(:,3) mydata.data(:,4) mydata.data(:,5) mydata.data(:,6)];

figure;

%% Import ApertureSurvey
apdirname = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/ApertureTest/10Mar16_HL/';
% original
apfile = 'Aperture_Survey_0.01_steps_OR_0_points.txt';
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


%% Remove 0 values from aperture file
%  for ii = 1:length(m_s)
%      if ((m_ap1(ii) == 0.0) && (m_ap2(ii) == 0.0) && (m_ap3(ii) == 0.0) && (m_ap4(ii) == 0.0))
%          m_ap1(ii) = NaN;
%          m_ap2(ii) = NaN;
%          m_ap3(ii) = NaN;
%          m_ap4(ii) = NaN;
%      end
% end

% m_ap=[m_s; m_ap1 ; m_ap2;  m_ap3; m_ap4];
% m_ap(~any( m_ap, 2 ), : ) = [];

index=find(~any( aperture, 2 )==0);
total=horzcat(mydata.data(:,1) ,aperture);
total=total(index,:);

%% Plot Aperture File
% plot(m_s, m_ap1, 'Color', 'red'), hold on
% plot(m_s, -m_ap3,'Color', 'red'), hold on

% plot(m_ap(:,1), m_ap(:,2), 'Color', 'red'), hold on
% plot(m_ap(:,1), -m_ap(:,4),'Color', 'red'), hold on

% Rectangle Half Height (vertical ap)
%plot(total(:,1),total(:,3), 'Color', 'red'), hold on
plot(total(:,1),-total(:,3), 'Color', 'red'), hold on

% Rectangle Half Width (horizontal ap)
plot(total(:,1),total(:,2), 'Color', 'blue'), hold on
%plot(total(:,1),-total(:,2), 'Color', 'blue'), hold on

%% Plot Aperture Survey

% Horizontal Aperture
plot(ap_s, ap_px, '--', 'Color', 'black'), hold on
%plot(ap_s, -ap_mx, '--' ,'Color', 'black'), hold on

% Vertical Aperture
%plot(ap_s, ap_py, '--' , 'Color', 'green'), hold on
plot(ap_s, -ap_my, '--' ,'Color', 'green'), hold on

axis([0,100,-0.1,0.1])

hold off