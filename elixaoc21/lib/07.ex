defmodule Day7 do
  def solve_1_eg do
    solve_1("input/input_07_eg.txt")
  end

  def solve_1_real do
    solve_1("input/input_07.txt")
  end

  def solve_2_eg do
    solve_2("input/input_07_eg.txt")
  end

  def solve_2_real do
    solve_2("input/input_07.txt")
  end

  def solve_1(filename) do
    initial_positions = get_initial_positions(filename)
    for x <- Enum.min(initial_positions)..Enum.max(initial_positions) do x end
    |> Enum.map(&get_fuel_cost_in_moving_to_position(&1, initial_positions))
    |> Enum.min
  end


  def solve_2(filename) do
    initial_positions = get_initial_positions(filename)
    for x <- Enum.min(initial_positions)..Enum.max(initial_positions) do x end
    |> Enum.map(&get_fuel_cost_in_moving_to_position_trig(&1, initial_positions))
    |> Enum.min
  end

  defp get_fuel_cost_in_moving_to_position(target_position, initial_positions) do
    Enum.map(initial_positions, fn x -> abs(x - target_position) end)
    |> Enum.sum
  end

  defp get_fuel_cost_in_moving_to_position_trig(target_position, initial_positions) do
    Enum.map(initial_positions, fn x ->
      abs(x - target_position) * (abs(x - target_position) + 1) / 2
    end)
    |> Enum.sum
  end

  defp get_initial_positions(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split(",")
    |> Enum.map(fn x -> Integer.parse(x) |> elem(0) end)
  end


end
