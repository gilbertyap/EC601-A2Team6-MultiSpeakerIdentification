clc;
clear all;
data = readmatrix('video6.csv');
data = data';
frameNums = data(1,:);
startIndex = 1;
offsets = [];
durations = [];
for i=1:length(frameNums)-1
  if (frameNums(i) ~= (frameNums(i+1)-1))
    % Sum all of the  previous frames into one offset
    offsets = [ offsets frameNums(startIndex)/25];
    durations = [ durations (frameNums(i)-frameNums(startIndex)+1)/25];
    startIndex = i+1;
  end
end
i = i +1;
if startIndex ~= i
    offsets = [ offsets frameNums(startIndex)/25];
    durations = [ durations (frameNums(i)-frameNums(startIndex))/25];
end
newData = [offsets; durations]'
writematrix(newData, 'video6_data.txt')