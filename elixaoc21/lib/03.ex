defmodule Day3 do
  def solve_1_eg do
    solve_1("input/input_03_eg.txt")
  end

  def solve_1_real do
    solve_1("input/input_03.txt")
  end

  def solve_2_eg do
    solve_2("input/input_03_eg.txt")
  end

  def solve_2_real do
    solve_2("input/input_03.txt")
  end

  def solve_1(filename) do
    input_list = File.read!(filename)
    |> get_input_from_file()
    output_list = Enum.reduce(input_list, &MostCommon.update_sum_with_element_of_list(&1, &2))
    get_gamma_rate(output_list, length(input_list)) * get_epsilon_rate(output_list, length(input_list))
  end

  def solve_2(filename) do
    input_list = File.read!(filename)
    |> get_input_from_file()

    oxy = MostCommon.get_elements_with_most_common_bit_in_pos(input_list, get_most_common_bits(input_list), 0, length(input_list))
    |> Enum.at(0)
    |> Integer.undigits(2)

    co2 = LeastCommon.get_elements_with_least_common_bit_in_pos(input_list, get_least_common_bits(input_list), 0, length(input_list))
    |> Enum.at(0)
    |> Integer.undigits(2)

    oxy * co2
  end

  defmodule Padding do
    def pad_to_fixed_binary_length(binary_list, desired_len) when length(binary_list) < desired_len do
      pad_to_fixed_binary_length([0] ++ binary_list, desired_len)
    end

    def pad_to_fixed_binary_length(binary_list, _) do
      binary_list
    end
  end

  defp get_input_from_file(file_content) do
    content_list = String.split(file_content, "\n", trim: true)
    len = byte_size(Enum.at(content_list, 0))
    Enum.map(content_list, &parse_element_and_pad_to_len(&1, len))
    |> (fn (x) -> [for _ <- 0..len do 0 end] ++ x end).()
  end

  defp parse_element_and_pad_to_len(element, len) do
    Integer.parse(element, 2)
    |> elem(0)
    |> Integer.digits(2)
    |> Padding.pad_to_fixed_binary_length(len)
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
    output_list = Enum.reduce(input_list, &MostCommon.update_sum_with_element_of_list(&1, &2))
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

  def get_least_common_bits(input_list) do
    most_common_bits = MostCommon.get_most_common_bits(input_list)
    Enum.map(most_common_bits, fn x -> case x do 0 -> 1; 1 -> 0 end end)
  end

end

defmodule MostCommon do
  def get_elements_with_most_common_bit_in_pos(input_list, desired_bits, position, initial_input_len_list) when (length(input_list) > 1) and (position < initial_input_len_list) do
    most_common_bits = get_most_common_bits(input_list)
    new_list = Enum.filter(input_list, fn (x) ->
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

  def update_sum_with_element_of_list(new_element, sum_list) do
    for idx <- 0..length(new_element)-1 do
      Enum.at(new_element, idx) + Enum.at(sum_list, idx)
    end
  end
end
