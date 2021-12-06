defmodule Day2Test do
  use ExUnit.Case
  test "Day 2 - 1" do
    assert Day2.solve_1_eg() == 150
    assert Day2.solve_1_real() == 2091984
  end
  test "Day 2 - 2" do
    assert Day2.solve_2_eg() == 900
    assert Day2.solve_2_real() == 2086261056
  end
end
