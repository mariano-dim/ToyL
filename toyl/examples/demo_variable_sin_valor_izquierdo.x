begin
    var S : int;
    S := 1;
    for T := 1 (to) 10 do
    begin
        #T := T + 1;
        S := S + 1 + T;
        print(-> T ->"  " ->S);
    end
end