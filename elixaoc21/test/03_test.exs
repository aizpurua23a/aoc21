defmodule Day3Test do
  use ExUnit.Case
  test "Day 3 - 1" do
    assert Day3.solve_1_eg() == 198
    assert Day3.solve_1_real() == 3912944
  end
  test "Day 3 - 2" do
    assert Day3.solve_2_eg() == 230
    assert Day3.solve_2_real() == 4996233
  end
end
