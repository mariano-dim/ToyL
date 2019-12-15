begin
    var Y : int;
    Y := 10;
    var U : int;
    while (Y > 9)
    begin

        U := 1;
        print(-> "valor de variable U: " -> U);
        print(-> "valor de variable Y: " -> Y);
        Y := Y - 1;
        var S : int; S := 1;
        while (S < 5)
        begin
            U := U+1;
            print(-> "valor de variable S : " -> S);
            S := S+1;
        end
    end
    print(-> "valor de variable U : " -> U);
end
