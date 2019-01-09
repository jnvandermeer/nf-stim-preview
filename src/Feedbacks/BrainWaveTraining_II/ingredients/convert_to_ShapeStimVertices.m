
% script to convert to (normalized) set of lines for LineStim:

% m=[import it...]

m(1,:) = [];
m(:,2)=-m(:,2);
newm=[];x=m(1,1);y=m(1,2);for i=1:size(m);xn = x + m(i,1);yn = y + m(i,2); newm(end+1,:)=[xn yn];x=xn;y=yn;end
nnewm=newm;
nnnewm=[];maxs=max(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2));for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(i,1)-mins(1)) by+scy*(nnewm(i,2)-mins(2))];end

figure;plot(nnnewm(:,1),nnnewm(:,2))



% 

% 
% 
% 
% x=m(1,1);y=m(1,2);figure;axes;for i=1:size(m);xn = x + m(i,1);yn = y + m(i,2); line([x xn],[y yn],'marker','x');x=xn;y=yn;end
% newm=[];x=m(1,1);y=m(1,2);figure;axes;for i=1:size(m);xn = x + m(i,1);yn = y + m(i,2); newm=[xn yn];line([x xn],[y yn],'marker','x');x=xn;y=yn;end
% figure;plot(newm(:,1),newm(:,2))
% newm
% 
% figure;plot(newm(:,1),newm(:,2))
% mean(newm)
% nnewm=newm-mean(newm)
% figure;plot(nnewm(:,1),nnewm(:,2))
% max(newm)
% max(mnewm)
% max(newm)
% max(nnewm)
% min(nnewm)
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2);for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1) by+scy*(nnewm(2)-mins(2)];end
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2);for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1)) by+scy*(nnewm(2)-mins(2))];end
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2);for i=1:size(nnewm,1); nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1)) by+scy*(nnewm(2)-mins(2))];end
% size(nnewm,1)
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2);for i=1:size(nnewm,1); 1;end
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2);for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1)) by+scy*(nnewm(2)-mins(2))];end
% nnnewm=[];maxs=maxs(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2));for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1)) by+scy*(nnewm(2)-mins(2))];end
% nnnewm=[];maxs=max(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2));for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(1)-mins(1)) by+scy*(nnewm(2)-mins(2))];end
% nnewm
% nnnewm
% nnnewm=[];maxs=max(nnewm);mins=min(nnewm);bx=-1;by=-1;scx=2/(maxs(1)-mins(1));scy=2/(maxs(2)-mins(2));for i=1:size(nnewm,1);nnnewm(end+1,:) = [bx+scx*(nnewm(i,1)-mins(1)) by+scy*(nnewm(i,2)-mins(2))];end
% nnewm
% nnnewm
