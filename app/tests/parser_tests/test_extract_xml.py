import pytest
import xlrd

from app.utils.parser.extract_xml import extract_report_data


class TestExtractReportData:
    def test_extract_report_data(self, mocker, mock_data, expected_result):
        mock_workbook = mocker.Mock(spec=xlrd.Book)
        mock_sheet = mocker.Mock()
        mock_sheet.nrows = len(mock_data)
        mock_sheet.row_values.side_effect = mock_data
        mock_workbook.sheet_by_index.return_value = mock_sheet

        mocker.patch("xlrd.open_workbook", return_value=mock_workbook)

        result = extract_report_data("dummy_path.xls")
        assert result == expected_result

    def test_extract_report_data_empty(self, mocker):
        mock_workbook = mocker.Mock(spec=xlrd.Book)
        mock_sheet = mocker.Mock()
        mock_sheet.nrows = 1
        mock_sheet.row_values.return_value = ["Единица измерения: Метрическая тонна"]
        mock_workbook.sheet_by_index.return_value = mock_sheet

        mocker.patch("xlrd.open_workbook", return_value=mock_workbook)

        result = extract_report_data("dummy_path.xls")
        assert result == []