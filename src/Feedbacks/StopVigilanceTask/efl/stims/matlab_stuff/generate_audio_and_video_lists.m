% dit wordt een scriptje om de audio en de video op te starten.

% dit ZOU een python-list-of-list-of-list moeten schrijven die je kan
% copy/pasten in python voor de localizer.

% en dit kan (heel mooi) ook uitgereid worden met letters.

all_audio = [10 20; 30 40; 50 60; 77.5 95; 112.5 130; 147.5 165; 175 185;195 205;215 225; 242.5 260;277.5 295;312.5 330];
audio_l = all_audio([1 3 5 8 10 12],:);
audio_r = all_audio([2 4 6 7 9 11 ],:);
audio_l_40 = audio_l([1 3 5],:);
audio_l_55 = audio_l([2 4 6],:);
audio_r_40 = audio_r([1 3 6],:);
audio_r_55 = audio_r([2 4 5],:);

audio_mat = cat(3,audio_l_40,audio_l_55,audio_r_40,audio_r_55);


all_video = [17.5 35;52.5 70;87.5 105;115 125;135 145;155 165;182.5 200;217.5 235;252.5 270;280 290;300 310;320 330];
video_l = all_video([1 3 5 8 10 12],:);
video_r = all_video([2 4 6 7 9 11 ],:);
video_l_8 = video_l([1 3 5],:);
video_l_13 = video_l([2 4 6],:);
video_r_8 = video_r([1 3 6],:);
video_r_13 = video_r([2 4 5],:);

video_mat = cat(3,video_l_8,video_l_13,video_r_8,video_r_13);



% make names, onsets, durations - for (later) fMRI analyses
names = {'audio_l','audio_r','video_l','video_r'};
onsets = {audio_l(:,1), audio_r(:,1), video_l(:,1), video_r(:,1)};
durations = {diff(audio_l,1,2), diff(audio_r,1,2), diff(video_l,1,2), diff(video_r,1,2)};


% write stuff for python (!)
sa='[';
for i=1:size(audio_mat,3)
    for j=1:size(audio_mat,1)
        switch i
            case 1
                action = 'audio';
                options = {'left','40'};
            case 2
                action = 'audio';
                options = {'left','55'};
            case 3
                action = 'audio';
                options = {'right','40'};
            case 4
                action = 'audio';
                options = {'right','55'};
        end
        
        
        tmp_1 = audio_mat(j,1,i);
        tmp_2 = audio_mat(j,2,i);
        if ~rem(tmp_1,1)
            tmp_1 = [sprintf('%g',tmp_1) '.'];
        else
            tmp_1 = [sprintf('%g',tmp_1) ''];
        end
        if ~rem(tmp_2,1)
            tmp_2 = [sprintf('%g',tmp_2) '.'];
        else
            tmp_2 = [sprintf('%g',tmp_2) ''];
        end
        
        sa = [sa sprintf('[%s,%s,\''%s\'',[',tmp_1,tmp_2,action)];
        
        for j=1:numel(options)
           sa=[sa sprintf('\''%s\'',',options{j})];
        end
        sa(end)=[];
        sa=[sa sprintf(']],')];
    end
end

for i=1:size(video_mat,3)
    for j=1:size(video_mat,1)
        switch i
            case 1
                action = 'video';
                options = {'left','8'};
            case 2
                action = 'video';
                options = {'left','13'};
            case 3
                action = 'video';
                options = {'right','8'};
            case 4
                action = 'video';
                options = {'right','13'};
        end
        
        tmp_1 = video_mat(j,1,i);
        tmp_2 = video_mat(j,2,i);
        if ~rem(tmp_1,1)
            tmp_1 = [sprintf('%g',tmp_1) '.'];
        else
            tmp_1 = [sprintf('%g',tmp_1) ''];
        end
        if ~rem(tmp_2,1)
            tmp_2 = [sprintf('%g',tmp_2) '.'];
        else
            tmp_2 = [sprintf('%g',tmp_2) ''];
        end
        
        sa = [sa sprintf('[%s,%s,\''%s\'',[',tmp_1,tmp_2,action)];
        for j=1:numel(options)
           sa=[sa sprintf('\''%s\'',',options{j})];
        end
        sa(end)=[];
        sa=[sa sprintf(']],')];
    end
end

sa(end)=[];
sa=[sa sprintf(']')];


