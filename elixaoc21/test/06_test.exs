defmodule Day6Test do
  use ExUnit.Case
  test "Day 6 - 1" do
    assert Day6.solve_1_eg() == 5934
    assert Day6.solve_1_real() == 388419
  end
  test "Day 6 - 2" do
    assert Day6.solve_2_eg() == 26984457539
    assert Day6.solve_2_real() == 1740449478328
    assert true
  end
end
