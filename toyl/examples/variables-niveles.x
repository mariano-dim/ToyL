# Programa utilizado para comprobar scope utilizando varios niveles
# Se compara con un programa similar en python

begin
    var Y: int;
    Y:=10;
    for e := 0 (to) 2 do
    begin
        print(->"Iniciando bloque interior");
        var P:int;
        P := 10 + e;
        while (Y>0)
        begin
            print(->"Iniciando bloque intermedio" ->Y);
            while(P>5)
            begin
                print(->"Iniciando bloque mas profundo " ->Y ->P);
                P := P-1;
            end
            Y := Y-1;
        end
    end
end
