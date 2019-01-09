% subtract 0.065 from each ISI time interval to account for the drag (~10
% seconds overall) of the async. This will match the gng ending to audio
% and visual endings, too.



d=dir('newparam_*txt');

for i=1:numel(d)
    
    fname=d(i).name;
    
    m=load(fname);
    
    m(:,3) = m(:,3) - 0.065;
    
    save(d(i).name,'m','-ascii');
    
    fprintf('Did: %s\n', d(i).name);
    
end

