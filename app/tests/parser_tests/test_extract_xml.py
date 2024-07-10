import pytest
from app.utils.parser.extract_xml import extract_report_data
import xlrd


class TestExtractReportData:
    @pytest.mark.parametrize(
        "mock_data, expected_result",
        [
            (
                [
                    ["Единица измерения: Метрическая тонна"],
                    [
                        "код инструмента",
                        "наименование инструмента",
                        "базис поставки",
                        "объем договоров в единицах измерения",
                        "обьем договоров, руб.",
                        "количество договоров, шт.",
                    ],
                    ["PROD001", "Product 1", "Basis 1", "100", "1000000", "10"],
                    ["PROD002", "Product 2", "Basis 2", "200", "2000000", "20"],
                ],
                [
                    {
                        "exchange_product_id": "PROD001",
                        "exchange_product_name": "Product 1",
                        "delivery_basis_name": "Basis 1",
                        "volume": 100.0,
                        "total": 1000000.0,
                        "count": 10,
                    },
                    {
                        "exchange_product_id": "PROD002",
                        "exchange_product_name": "Product 2",
                        "delivery_basis_name": "Basis 2",
                        "volume": 200.0,
                        "total": 2000000.0,
                        "count": 20,
                    },
                ],
            ),
        ],
    )
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
