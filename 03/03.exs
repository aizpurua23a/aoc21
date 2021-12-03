# Day 3 - 1
use Bitwise

defmodule Padding do
  def pad_to_fixed_binary_length(binary_list, desired_len) when length(binary_list) < desired_len do
    pad_to_fixed_binary_length([0] ++ binary_list, desired_len)
  end

  def pad_to_fixed_binary_length(binary_list, _) do
    binary_list
  end
end


defmodule Day3 do
  defmodule MostCommon do
    def get_elements_with_most_common_bit_in_pos(input_list, desired_bits, position, initial_input_len_list) when (length(input_list) > 1) and (position < initial_input_len_list) do
      most_common_bits = Day3.get_most_common_bits(input_list)
      #IO.inspect most_common_bits
      new_list = Enum.filter(input_list, fn (x) ->
        #IO.inspect [x, most_common_bits, position]
        Enum.at(x, position) == Enum.at(most_common_bits, position)
      end)
      get_elements_with_most_common_bit_in_pos(new_list, desired_bits, position + 1, initial_input_len_list)
    end
    def get_elements_with_most_common_bit_in_pos(input_list, _, _, _) when (length(input_list) == 1) do
      input_list
    end
    def get_elements_with_most_common_bit_in_pos(_, _, _, _) do
      IO.inspect "Something went wrong"
    end

  end

  defmodule LeastCommon do
    def get_elements_with_least_common_bit_in_pos(input_list, desired_bits, position, initial_input_len_list) when (length(input_list) > 1) and (position < initial_input_len_list) do
      least_common_bits = Day3.get_least_common_bits(input_list)
      #IO.inspect least_common_bits
      new_list = Enum.filter(input_list, fn (x) ->
        #IO.inspect [x, least_common_bits, position]
        Enum.at(x, position) == Enum.at(least_common_bits, position)
      end)
      get_elements_with_least_common_bit_in_pos(new_list, desired_bits, position + 1, initial_input_len_list)
    end
    def get_elements_with_least_common_bit_in_pos(input_list, _, _, _) when (length(input_list) == 1) do
      input_list
    end
    def get_elements_with_least_common_bit_in_pos(_, _, _, _) do
      IO.inspect "Something went wrong"
    end

  end

  defp parse_element_and_pad_to_len(element) do
    Integer.parse(element, 2)
    |> elem(0)
    |> Integer.digits(2)
    #|> Padding.pad_to_fixed_binary_length(5)
    |> Padding.pad_to_fixed_binary_length(12)
  end


  defp get_input_from_file(file_content) do
    String.split(file_content, "\n", trim: true)
    |> Enum.map(&parse_element_and_pad_to_len(&1))
    #|> (fn (x) -> [[0, 0, 0, 0, 0]] ++ x end).()
    |> (fn (x) -> [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] ++ x end).()
  end

  defp update_sum_with_element_of_list(new_element, sum_list) do
    for idx <- 0..length(new_element)-1 do
      Enum.at(new_element, idx) + Enum.at(sum_list, idx)
    end
  end

  defp get_gamma_rate(output_list, input_len) do
    Enum.map(output_list, fn (x) ->
      boolean_value = x > input_len/2
      case boolean_value do
        true -> 1
        false -> 0
      end
    end)
    |> Integer.undigits(2)
  end

  defp get_epsilon_rate(output_list, input_len) do
    Enum.map(output_list, fn (x) ->
      boolean_value = x < input_len/2
      case boolean_value do
        true -> 1
        false -> 0
      end
    end)
    |> Integer.undigits(2)
  end

  def get_most_common_bits(input_list) do
    output_list = Enum.reduce(input_list, &update_sum_with_element_of_list(&1, &2))
    Enum.map(output_list, fn (x) ->
      boolean_value = x >= length(input_list)/2
      case boolean_value do
        true -> 1
        false -> 0
      end
    end)
  end

  def get_least_common_bits(input_list) do
    most_common_bits = get_most_common_bits(input_list)
    Enum.map(most_common_bits, fn x -> case x do 0 -> 1; 1 -> 0 end end)
  end

  def part1() do
    input_list = File.read!("input_01.txt")
    |> get_input_from_file()

    output_list = Enum.reduce(input_list, &update_sum_with_element_of_list(&1, &2))
    IO.inspect get_gamma_rate(output_list, length(input_list)) * get_epsilon_rate(output_list, length(input_list))
  end

  def part2() do
    input_list = File.read!("input_01.txt")
    |> get_input_from_file()
    oxy = MostCommon.get_elements_with_most_common_bit_in_pos(input_list, get_most_common_bits(input_list), 0, length(input_list))
    |> Enum.at(0)
    |> Integer.undigits(2)
    |> IO.inspect

    co2 = LeastCommon.get_elements_with_least_common_bit_in_pos(input_list, get_least_common_bits(input_list), 0, length(input_list))
    |> Enum.at(0)
    |> Integer.undigits(2)
    |> IO.inspect

    IO.inspect oxy * co2
  end
end

#Day3.part1()
Day3.part2()
