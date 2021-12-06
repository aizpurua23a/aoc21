# Day 2 - 1

defmodule Day2 do
  def solve_1_eg do
    solve_1("input/input_02_eg.txt")
  end

  def solve_1_real do
    solve_1("input/input_02.txt")
  end

  def solve_2_eg do
    solve_2("input/input_02_eg.txt")
  end

  def solve_2_real do
    solve_2("input/input_02.txt")
  end

  def solve_1(filename) do
    File.read!(filename)
    |> get_list_of_instructions_from_file()
    |> Enum.map(&create_map_for_solution(&1))
    |> append_first_dummy_element()
    |> Enum.reduce(&reduce_to_get_final_position(&1, &2))
    |> (fn (x) -> x[:depth] * x[:horizontal]end).()
  end

  def solve_2(filename) do
    File.read!(filename)
    |> get_list_of_instructions_from_file()
    |> Enum.map(&create_map_for_solution_with_aim(&1))
    |> append_first_dummy_element_with_aim()
    |> Enum.reduce(&reduce_to_get_final_position_with_aim(&1, &2))
    |> (fn (x) -> x[:depth] * x[:horizontal]end).()
  end

  defp get_list_of_instructions_from_file(file_content) do
    String.split(file_content, "\n", trim: true)
    |> Enum.map(fn (x) -> String.split(x, " ") end)
    |> Enum.map(fn (x) -> [Enum.at(x, 0), elem(Integer.parse(Enum.at(x, 1)), 0)]end)
  end

  defp create_map_for_solution(instruction_tuple) do
    %{
      instruction: Enum.at(instruction_tuple, 0),
      num: Enum.at(instruction_tuple, 1),
      depth: 0,
      horizontal: 0
    }
  end

  defp append_first_dummy_element(instruction_list) do
    [%{depth: 0, horizontal: 0}] ++ instruction_list
  end

  defp append_first_dummy_element_with_aim(instruction_list) do
    [%{depth: 0, horizontal: 0, aim: 0}] ++ instruction_list
  end

  defp reduce_to_get_final_position(new_step, position_so_far) do
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
  end

  defp reduce_to_get_final_position_with_aim(new_step, position_so_far) do
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
  end

  defp create_map_for_solution_with_aim(instruction_tuple) do
    %{
      instruction: Enum.at(instruction_tuple, 0),
      num: Enum.at(instruction_tuple, 1),
      depth: 0,
      horizontal: 0,
      aim: 0
    }
  end

end
