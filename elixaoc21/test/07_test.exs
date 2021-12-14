defmodule Day6Test do
  use ExUnit.Case
  test "Day 7 - 1" do
    assert Day7.solve_1_eg() == 37
    assert Day7.solve_1_real() == 344605
  end
  test "Day 7 - 2" do
    assert Day7.solve_2_eg() == 168
    assert Day7.solve_2_real() == 93699985
    assert true
  end
end
