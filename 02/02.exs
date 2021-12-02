# Day 2 - 1

get_list_of_instructions_from_file = fn (file_content) ->
  String.split(file_content, "\n", trim: true)
  |> Enum.map(fn (x) -> String.split(x, " ") end)
  |> Enum.map(fn (x) -> [Enum.at(x, 0), elem(Integer.parse(Enum.at(x, 1)), 0)]end)
end

create_map_for_solution = fn (instruction_tuple) ->
  %{
    instruction: Enum.at(instruction_tuple, 0),
    num: Enum.at(instruction_tuple, 1),
    depth: 0,
    horizontal: 0
  } end

append_first_dummy_element = fn (instruction_list) -> [%{depth: 0, horizontal: 0}] ++ instruction_list end

reduce_to_get_final_position = fn (new_step, position_so_far) ->
  case new_step[:instruction] do
    "forward" ->
      %{
        horizontal: position_so_far[:horizontal] + new_step[:num],
        depth: position_so_far[:depth]
      }
    "up" ->
      %{
        horizontal: position_so_far[:horizontal],
        depth: position_so_far[:depth] - new_step[:num]
      }
    "down" ->
      %{
        horizontal: position_so_far[:horizontal],
        depth: position_so_far[:depth] + new_step[:num]
      }
    "_" ->
      IO.puts "Wrong instruction, no forward, up or down."
  end
  #|> IO.inspect
end


File.read!("input_01.txt")
|> get_list_of_instructions_from_file.()
|> Enum.map(create_map_for_solution)
|> append_first_dummy_element.()
|> Enum.reduce(reduce_to_get_final_position)
|> (fn (x) -> x[:depth] * x[:horizontal]end).()
|> IO.inspect


# Day 2 - 2

create_map_for_solution_with_aim = fn (instruction_tuple) ->
  %{
    instruction: Enum.at(instruction_tuple, 0),
    num: Enum.at(instruction_tuple, 1),
    depth: 0,
    horizontal: 0,
    aim: 0
  }
end

append_first_dummy_element_with_aim = fn (instruction_list) -> [%{depth: 0, horizontal: 0, aim: 0}] ++ instruction_list end

reduce_to_get_final_position_with_aim = fn (new_step, position_so_far) ->
  case new_step[:instruction] do
    "forward" ->
      %{
        horizontal: position_so_far[:horizontal] + new_step[:num],
        depth: position_so_far[:depth] + position_so_far[:aim] * new_step[:num],
        aim: position_so_far[:aim]
      }
    "up" ->
      %{
        horizontal: position_so_far[:horizontal],
        depth: position_so_far[:depth],
        aim: position_so_far[:aim] - new_step[:num]
      }
    "down" ->
      %{
        horizontal: position_so_far[:horizontal],
        depth: position_so_far[:depth],
        aim: position_so_far[:aim] + new_step[:num]
      }
    "_" ->
      IO.puts "Wrong instruction, no forward, up or down."
  end
  #|> IO.inspect
end



File.read!("input_01.txt")
|> get_list_of_instructions_from_file.()
|> Enum.map(create_map_for_solution_with_aim)
|> append_first_dummy_element_with_aim.()
|> Enum.reduce(reduce_to_get_final_position_with_aim)
|> (fn (x) -> x[:depth] * x[:horizontal]end).()
|> IO.inspect
