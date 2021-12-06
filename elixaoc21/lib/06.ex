defmodule Day6 do
  def solve_1_eg do
    solve_1("input/input_06_eg.txt")
  end

  def solve_1_real do
    solve_1("input/input_06.txt")
  end

  def solve_2_eg do
    solve_2("input/input_06_eg.txt")
  end

  def solve_2_real do
    solve_2("input/input_06.txt")
  end

  def solve_1(filename) do
    Enum.reduce(for _ <- 1..80 do 0 end, get_initial_population_map(filename), &simulate_day(&1, &2))
    |> Enum.map(fn x -> elem(x, 1) end)
    |> Enum.sum()
  end

  def solve_2(filename) do
    Enum.reduce(for _ <- 1..256 do 0 end, get_initial_population_map(filename), &simulate_day(&1, &2))
    |> Enum.map(fn x -> elem(x, 1) end)
    |> Enum.sum()
  end

  defp get_initial_population_map(filename) do
    pop_map = File.read!(filename)
    |> String.trim()
    |> String.split(",")
    |> Enum.map(fn x -> Integer.parse(x) |> elem(0) end)
    |> Enum.reduce(%{}, fn x, acc -> Map.update(acc, x, 1, &(&1 + 1)) end)

    Enum.reduce(for x <- 0..8 do x end, pop_map, fn (x, acc) -> Map.update(acc, x, 0, fn x -> x end) end)
  end

  defp simulate_day(_, accumulator) do
    for x <- 0..8 do
      case x do
        0 -> {0, Map.get(accumulator, 1)}
        1 -> {1, Map.get(accumulator, 2)}
        2 -> {2, Map.get(accumulator, 3)}
        3 -> {3, Map.get(accumulator, 4)}
        4 -> {4, Map.get(accumulator, 5)}
        5 -> {5, Map.get(accumulator, 6)}
        6 -> {6, Map.get(accumulator, 0) + Map.get(accumulator, 7)}
        7 -> {7, Map.get(accumulator, 8)}
        8 -> {8, Map.get(accumulator, 0)}
      end
    end
    |> Enum.into(%{})
  end
end
