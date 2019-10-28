begin
var x : int;
x := 12 + 3;
# Comentario x = 15
var t : int;
t := 20;
if (t > 25)
begin
    x := x * t;
end
else
begin
    if (x > 10)
    begin
        x := t;
    end
end
print(x);
print(t);
print(50+x);
print(16);
end