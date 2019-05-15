%% Plot ellipses and circles to test HEL elliptical matching

%% Ellipse
a=1.1; % horizontal radius
b=1; % vertical radius
x0=0; % x0,y0 ellipse centre coordinates
y0=0;
t=-pi:0.01:pi;
x=x0+a*cos(t);
y=y0+b*sin(t);
plot(x,y,'linewidth',1, 'linestyle', '-')
hold on

%% Old Circle
it=-pi:0.01:pi;
ix=a*cos(it);
iy=a*sin(it);
plot(ix,iy,'linewidth',1, 'linestyle', ':')
hold on

%% Shifted Circle
J = 1;
r = ((a*a + b*b)/2*b) * J;
xf=0; % x0,y0 circle centre coordinates
yf = (b - r);
tf=-pi:0.01:pi;
cx=xf+r*cos(tf);
cy=yf+r*sin(tf);
plot(cx,cy,'linewidth',1, 'linestyle', '--')
hold on


%% Scaled and Shifted Circle
J = sqrt(a/b);
r = ((a*a + b*b)/2*b) * J;
xf=0; % x0,y0 circle centre coordinates
yf = (b - r);
tf=-pi:0.01:pi;
cx=xf+r*cos(tf);
cy=yf+r*sin(tf);
plot(cx,cy,'linewidth',1, 'linestyle', '-')
hold on

xlabel('x [sigma]');
ylabel('y [sigma]');
grid on
axis equal
axis square
hold off