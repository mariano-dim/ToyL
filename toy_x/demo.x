begin
    var s: int;
    s:= 1;
    while (s <5)
    begin
        print(s);
        s := s+1;
    end

    for e := 1 (to) 2 do
    begin
        for f := 1 (to) 2 do
        begin
            print(f);
        end
        print(e);
    end

    if (s > 4)
    begin
        var cadena : string;
        cadena := "hola mundo";
        print(cadena);
    end

    var minus : int;
    minus := -1;
    print(minus);
    minus := -minus ;
    print(minus);

end