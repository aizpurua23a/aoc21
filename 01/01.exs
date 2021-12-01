#Day 1 - 1
get_list_of_deltas = fn (list_of_ints) ->
  for idx <- 0..length(list_of_ints)-2 do
    Enum.at(list_of_ints, idx + 1) - Enum.at(list_of_ints, idx)
  end
end

File.read!("input_01.txt")
|> String.split("\n", trim: true)
|> Enum.map(fn x -> case Integer.parse(x) do {int, _} -> int; _ -> nil end; end)
|> get_list_of_deltas.()
|> Enum.filter(fn (x) -> x > 0 end)
|> length
|> IO.inspect

#Day 1 - 2
#we ignore the first 2 and last 2 windows
#we only compare elements i with i+3, as i+1 and i+2 are shared:
# (x(i+3) + x(i+2) + x(i+1)) - (x(i) + x(i+1) + x(i+2)) = x(i+3) - x(i), ignoring 0, 1, -2 and -1

get_list_of_three_measuring_window_deltas = fn (list_of_ints) ->
  for idx <- 0..length(list_of_ints)-4 do
    Enum.at(list_of_ints, idx+3) - Enum.at(list_of_ints, idx)
  end
end

File.read!("input_01.txt")
|> String.split("\n", trim: true)
|> Enum.map(fn x -> case Integer.parse(x) do {int, _} -> int; _ -> nil end; end)
|> get_list_of_three_measuring_window_deltas.()
|> Enum.filter(fn (x) -> x > 0 end)
|> length
|> IO.inspect
