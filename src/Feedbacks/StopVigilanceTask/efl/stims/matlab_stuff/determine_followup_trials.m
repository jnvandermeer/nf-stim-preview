function gather = determine_followup_trials(in)


gather = zeros(size(in,1),1);
curlen=0;

for i=1:numel(in)
    cur=in(i);
    
    if cur == 0
        if curlen > 0
            gather(curlen) = gather(curlen) + 1;
        end
        reset = 1;
        curlen = 0;
    else
        curlen = curlen + 1;
        reset = 0;
        
    end
end

% return gather

