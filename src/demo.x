begin
var x : int;
x := 12 + 3;
# Comentario x = 15
var t : int;
t := 25;
if (t = 25)
begin
    x := x * t;
end
else
begin
    x := 1 + t;
    if (10  < 1)
    begin
        x := 5;
    end
end
print(x);
print(t);
print(16);
end