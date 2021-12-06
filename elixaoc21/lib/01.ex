#Day 1 - 1

defmodule Day1 do
  def solve_1_eg do
    solve_1("input/input_01_eg.txt")
  end

  def solve_1_real do
    solve_1("input/input_01.txt")
  end

  def solve_2_eg do
    solve_2("input/input_01_eg.txt")
  end

  def solve_2_real do
    solve_2("input/input_01.txt")
  end

  def solve_1(filename) do
    File.read!(filename)
    |> String.split("\n", trim: true)
    |> Enum.map(fn x -> case Integer.parse(x) do {int, _} -> int; _ -> nil end; end)
    |> get_list_of_deltas()
    |> Enum.filter(fn (x) -> x > 0 end)
    |> length
  end

  def solve_2(filename) do
    File.read!(filename)
    |> String.split("\n", trim: true)
    |> Enum.map(fn x -> case Integer.parse(x) do {int, _} -> int; _ -> nil end; end)
    |> get_list_of_three_measuring_window_deltas()
    |> Enum.filter(fn (x) -> x > 0 end)
    |> length
  end

  defp get_list_of_deltas(list_of_ints) do
    for idx <- 0..length(list_of_ints)-2 do
      Enum.at(list_of_ints, idx + 1) - Enum.at(list_of_ints, idx)
    end
  end

  defp get_list_of_three_measuring_window_deltas(list_of_ints) do
    for idx <- 0..length(list_of_ints)-4 do
      Enum.at(list_of_ints, idx+3) - Enum.at(list_of_ints, idx)
    end
  end
end
