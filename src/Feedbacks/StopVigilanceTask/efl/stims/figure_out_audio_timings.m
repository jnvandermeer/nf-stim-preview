diff(inds_high(diff(inds_high)>2))/44100
44100/diff(inds_high(diff(inds_high)>2))
44100./diff(inds_high(diff(inds_high)>2))
mean(44100./diff(inds_high(diff(inds_high)>2)))
inds=(diff(a.data) > 0.5_
inds=(diff(a.data) > 0.5)
inds>0.5
inds(:,1)
inds(1:10,:)
diff(a.data(:,1))
find(diff(a.data(:,1)) > 0.5)
[1;find(diff(a.data(:,1)) > 0.5)]
a
44100/[1;find(diff(a.data(:,1)) > 0.5)]
44100./[1;find(diff(a.data(:,1)) > 0.5)]
round(44100./[1;find(diff(a.data(:,1)) > 0.5)])
[1;find(diff(a.data(:,1)) > 0.5)]
a
[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100)
ceil([1;find(diff(a.data(:,1)) > 0.5)]*(1/44100))
[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100)
[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100)*1000
ceil([1;find(diff(a.data(:,1)) > 0.5)]*(1/44100)*1000)
ceil([1;find(diff(a.data(:,1)) > 0.5)]*(1/44100))
[1;find(diff(a.data(:,1)) > 0.5)]
[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100)
ts=[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100);
save audio_40_ts.txt ts -ascii
type audio_40_ts.txt
a=importdata('audio_40Hz_R.wav');
ts2=[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100);
ts
ts2
ts2=[1;find(diff(a.data(:,2)) > 0.5)]*(1/44100);
ts2
ts-ts2
a=importdata('audio_55Hz_L.wav');
ts=[1;find(diff(a.data(:,1)) > 0.5)]*(1/44100);
ts
save audio_55_ts.txt ts -ascii
ts2=[1;find(diff(a.data(:,2)) > 0.5)]*(1/44100);
ts2
a=importdata('audio_55Hz_R.wav');
ts2=[1;find(diff(a.data(:,2)) > 0.5)]*(1/44100);
ts-ts2
ts
diff(ts)
1000/diff(ts)
1000./diff(ts)
diff(ts)
ts
ts*1000
diff(ts)
diff(ts)*1000
diff(ts)
1000/diff(ts)
1000/(diff(ts))
1000./(diff(ts))
1./(diff(ts))
mean(1./(diff(ts)))
unique(1./(diff(ts)))
load audio_55_ts.txt
audio_55_ts
load audio_40_ts.txt
audio_40_ts
diff(audio_40_ts)
diff(audio_40_ts).^-1
unique(diff(audio_40_ts).^-1)
whos
whos audio_40_ts
whos audio_55_ts
55/43
55/32
55/40
copyfile audio_40_ts.txt ~/repos/pyff/try/stims/.
ls
history