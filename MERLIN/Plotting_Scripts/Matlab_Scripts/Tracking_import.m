%% Import data from text file.
%% Initialize variables.
tdir = '/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/SymplecticLossMap/Test/';
tfile = 'Tracking_output_file100_1.txt';
tfilename = strcat(tdir,tfile);
delimiter = ' ';
startRow = 2;

%% Format string for each line of text:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%f%f%f%f%f%f%f%f%f%[^\n\r]';

%% Open the text file.
tfileID = fopen(tfilename,'r');

%% Read columns of data according to format string.
dataArray = textscan(tfileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);

%% Close the text file.
fclose(tfileID);

%% Allocate imported array to column variable names
t_id = dataArray{:, 1};
t_turn = dataArray{:, 2};
t_s = dataArray{:, 3};
t_x = dataArray{:, 4};
t_xp = dataArray{:, 5};
t_y = dataArray{:, 6};
t_yp = dataArray{:, 7};
t_dp = dataArray{:, 8};
t_type = dataArray{:, 9};

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec tfileID tfile tdir dataArray ans;