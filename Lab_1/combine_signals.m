function signal = combine_signals(s1,s2);
% function taes two signals s1 and s2, 
% adds them together into a composite signal, 
% then plots the composite signal
% with the original signals dotted in the background
    signal = s1 + s2;
    plot(s1(1:100),"LineStyle","-.");
    hold on;
    plot(s2(1:100),"LineStyle","-.");
    hold on;
    plot(signal(1:100),"LineWidth",1.0,"Color",[0,0,0]);
    hold off;
    set(gca,'XGrid','off','YGrid','on');
    title('Combined Signal');
    xlabel('Sample');
    ylabel('Amplitude')
end