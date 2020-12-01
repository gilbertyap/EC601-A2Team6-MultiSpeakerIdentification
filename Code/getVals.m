clc;
clear all;
data = readmatrix('video1.csv');
data = data';
lumVals = data(2,:);
lumVals(find(lumVals > 90)) = [];
histogram(lumVals);
rounded = round(lumVals);
mean(rounded)
mode(rounded)
mean(rounded)+(0.75*sqrt(var(rounded)))