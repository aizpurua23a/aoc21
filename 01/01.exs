#Day 1 - 1
get_list_of_deltas = fn (list_of_ints) ->
  for idx <- 0..length(list_of_ints)-2 do
    Enum.at(list_of_ints, idx + 1) - Enum.at(list_of_ints, idx)
  end
end

File.read!("input_01.txt")
|> String.split("\n", trim: true)
|> Enum.map(fn x -> Integer.parse(x) |> Tuple.to_list |> Enum.at(0) end)
|> get_list_of_deltas.()
|> Enum.filter(fn (x) -> x > 0 end)
|> length
|> IO.inspect

#Day 1 - 2
get_list_of_three_measuring_window = fn (list_of_ints) ->
  for idx <- 0..length(list_of_ints)-3 do
    Enum.at(list_of_ints, idx) + Enum.at(list_of_ints, idx + 1) + Enum.at(list_of_ints, idx + 2)
  end
end

File.read!("input_01.txt")
|> String.split("\n", trim: true)
|> Enum.map(fn x -> Integer.parse(x) |> Tuple.to_list |> Enum.at(0) end)
|> get_list_of_three_measuring_window.()
|> get_list_of_deltas.()
|> Enum.filter(fn (x) -> x > 0 end)
|> length
|> IO.inspect
