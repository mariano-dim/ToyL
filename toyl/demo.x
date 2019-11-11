# Programa utilizado para comprobar scope utilizando varios niveles
# Se compara con un programa similar en python

begin
    var Y: int;
    var P:int;
    var J : int;
    #J := 100;
    Y:=10;

    for e := 0 (to) 2 do
    begin
        print(->"Iniciando bloque interior");

        P := 10 + e;

        while (Y>0)
        begin
            print(->"Iniciando bloque intermedio " ->Y);
            while(P>5)
            begin
                print(->"Iniciando bloque mas profundo " ->Y ->P);

                P := P-1;

                exec
                begin
                    print(-> "Dentro de bloque, valor de J " -> J);
                    var J : int;
                    J := 10;
                    print(-> "Dentro de bloque, valor de J " -> J);
                end

                # En este caso estoy definiendo reiteradamente el mismo ID para el mismo scope

                J := 1;

            end

            Y := Y-1;
        end
    end
end
