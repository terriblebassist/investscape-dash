from scripts import historicalnav


class Test_historical_nav:
    def test_getFormattedDate(self):
        assert historicalnav.getFormattedDate('01-02-2020') == '2020-02-01'

    def test_modifyDateToWorkingDay(self):
        mockNavMap = {
            '2021-03-26' : '50.00'
        }
        assert historicalnav.modifyDateToWorkingDay('2021-03-27', mockNavMap) == '2021-03-26'
        assert historicalnav.modifyDateToWorkingDay('2021-03-28', mockNavMap) == '2021-03-26'

    def test_getHistoricalNavMap(self, mocker):
        mockSchemeCode = 118989
        jsonResponse = {
            'data' : [
                {'date' : '01-02-2021', 'nav' : '50.00'}, 
                {'date' : '02-02-2021', 'nav' : '51.00'}
            ]
        }
        mocker.patch('scripts.historicalnav.get_response_json_from_url', return_value=jsonResponse) 
        navMap = historicalnav.getHistoricalNavMap([mockSchemeCode])
        assert len(navMap) == 1
        assert len(navMap[mockSchemeCode]) == 2

    def test_getNavForDate(self, mocker):
        mockSchemeCode = '118989'
        mockNavMap = {
            '118989' : {
                '2021-02-01' : '50.00',
                '2021-02-02' : '52.00'
            }
        }
        mocker.patch('scripts.historicalnav.modifyDateToWorkingDay', return_value='2021-02-02')
        
        assert historicalnav.getNavForDate(mockNavMap, mockSchemeCode, '2021-02-01') == 50.00
        assert historicalnav.getNavForDate(mockNavMap, mockSchemeCode, '2021-02-03') == 52.00
