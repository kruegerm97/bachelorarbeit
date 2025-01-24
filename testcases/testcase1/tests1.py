# import pytest
# from unittest.mock import MagicMock




# def test_process_csv(mocker):
#     # Mock für pandas-Funktionen
#     mock_read_csv = mocker.patch("script.pd.read_csv", return_value=MagicMock())
#     mock_sort_values = mocker.patch("script.pd.DataFrame.sort_values", return_value=MagicMock())
#     mock_to_csv = mocker.patch("script.pd.DataFrame.to_csv")

#     # Funktion aufrufen
#     script.process_csv("input.csv", "output.csv")

#     # Tests
#     mock_read_csv.assert_called_once_with("input.csv")
#     mock_sort_values.assert_called_once_with(by="column_name")
#     mock_to_csv.assert_called_once_with("output.csv", index=False)
