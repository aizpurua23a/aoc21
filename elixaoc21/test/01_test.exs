defmodule Day1Test do
  use ExUnit.Case
  test "Day 1 - 1" do
    assert Day1.solve_1_eg() == 7
    assert Day1.solve_1_real() == 1298
  end
  test "Day 1 - 2" do
    assert Day1.solve_2_eg() == 5
    assert Day1.solve_2_real() == 1248
  end
end
