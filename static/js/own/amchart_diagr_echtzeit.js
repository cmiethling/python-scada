/**
 * Created by Karsten on 02.05.2017.
 */


$(document).ready(function () {
    //muss fuer die gesamte amchart_diagr_echtzeit.js sichtbar sein
    var chart = [];

    function diagramm_data(callback) {
        $.ajax({
            url: '/diagramm_data_1s',
            type: 'GET',

            success: function (response) {
                callback(response);
            }
        });
    }

//wird nur aufgerufen wenn diagramm_data(callback) fertig ist (siehe Zeile 265)
    function generateChartData(chartData) {
        // console.log(chartData);
        var dashlength = 5;
        chart = AmCharts.makeChart("chartdiv", {
            "type": "serial",
            "theme": "light",
            "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
            "legend": {
                "useGraphSettings": true
            },
            "dataProvider": chartData,
            "synchronizeGrid": true,
            "valueAxes": [
                {
                    "id": "v1",
                    "axisColor": "#FF6600",
                    "axisThickness": 2,
                    "axisAlpha": 1,
                    "position": "left",
                    "title": "Re: LF, TOC, N_ges, Trueb, Redox;  VB: TOC_errech",
                },
                {
                    "id": "v2",
                    "axisColor": "#FCD202",
                    "axisThickness": 2,
                    "axisAlpha": 1,
                    "position": "right",
                    "title": "pH; Vega;  Re: Zul, Temp; BR: Gas, Temp",
                },
                 {
                    "id": "v3",
                    "axisColor": "#6f00de",
                    "offset": 80,
                    "axisAlpha": 1,
                    "position": "right",
                    "axisThickness": 2,
                    "integersOnly": 1,
                    "maximum": 2,
                    "title": "P1, P2",
                },
            ],

            "graphs": [
                //Rechen
                {
                    "valueAxis": "v2",
                    // "hidden": true,
                    "lineColor": "#00e8f7",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_Zul (m³/h)",
                    "valueField": "MID",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#ff0e00",
                    "bullet": "round",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_pH1",
                    "valueField": "pH1",
                    "type": "smoothedLine",
                    "fillAlphas": 0
                },
                {
                    "valueAxis": "v1",
                    "hidden": true,
                    "lineColor": "#de7a00",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_LF (mS/cm)",
                    "valueField": "LF",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },
                {
                    "valueAxis": "v1",
                    "lineColor": "#000000",
                    "bullet": "round",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_TOC (mg/l)",
                    "valueField": "TOC",
                    "type": "smoothedLine",
                    "fillAlphas": 0
                },
                {
                    "valueAxis": "v1",
                    "hidden": true,
                    "lineColor": "#898989",
                    "bullet": "round",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_Nges (mg/l)",
                    "valueField": "N_ges",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },
                {
                    "valueAxis": "v1",
                    "hidden": true,
                    "lineColor": "#a2fc00",
                    "bullet": "square",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_Redox (mV)",
                    "valueField": "Redox",
                    "type": "smoothedLine",
                    "fillAlphas": 0
                },
                {
                    "valueAxis": "v1",
                    // "hidden": true,
                    "lineColor": "#8b4513",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_Trueb (FNU)",
                    "valueField": "Truebung",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },

                // V2.01 Nachtrag: Rechen Temperatur
                {
                    "valueAxis": "v2",
                    // "hidden": true,
                    "lineColor": "#00017a",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_Temp (°C)",
                    "valueField": "Temp_Re",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },

                // Vorlagebehaelter
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#6f00de",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "VB_pH2",
                    "valueField": "pH2",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },
                {
                    "valueAxis": "v2",
                    // "hidden": true,
                    "lineColor": "#0037de",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "VB_Vega1 (cm)",
                    "valueField": "Vega1",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },

                // V1.20 Nachtrag: Vega1 in l
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#0037de",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "VB_Vega1 (l)",
                    "valueField": "Vega1_l",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },

                {
                    "valueAxis": "v1",
                    // "hidden": true,
                    "lineColor": "#000000",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "VB_c_TOC_Vorl (mg/l)",
                    "valueField": "c_TOC_Vorlage",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },
                //Reaktor
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#8b4513",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "BR_pH3",
                    "valueField": "pH3",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },
                {
                    "valueAxis": "v2",
                    // "hidden": true,
                    "lineColor": "#1cde00",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "BR_Vega2 (mbar)",
                    "valueField": "Vega2",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#00017a",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "BR_Temp (°C)",
                    "valueField": "Temp",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                },
                {
                    "valueAxis": "v2",
                    "hidden": true,
                    "lineColor": "#00e8f7",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "BR_Gas (l)",
                    "valueField": "Gas",
                    "type": "smoothedLine",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },

                //    Pumpen
                {
                    "valueAxis": "v3",
                    // "hidden": true,
                    "lineColor": "#6f00de",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "Re_P1",
                    "valueField": "P1_EIN",
                    "type": "step",
                    "fillAlphas": 0,
                    "dashLength": dashlength,
                },
                {
                    "valueAxis": "v3",
                    // "hidden": true,
                    "lineColor": "#898989",
                    "bullet": "triangleUp",
                    "bulletBorderThickness": 1,
                    "hideBulletsCount": 30,
                    "title": "P2",
                    "valueField": "P2_EIN",
                    "type": "step",
                    "fillAlphas": 0,
                    // "dashLength": dashlength,
                },
            ],
            "chartScrollbar": {
                "oppositeAxis": false,
                "offset": 30,
                "scrollbarHeight": 20,
                "backgroundAlpha": 0,
                "selectedBackgroundAlpha": 0.1,
                "selectedBackgroundColor": "#888888",
                "graphFillAlpha": 0,
                "graphLineAlpha": 0.5,
                "selectedGraphFillAlpha": 0,
                "selectedGraphLineAlpha": 1,
                "autoGridCount": true,
                "color": "#AAAAAA"
            },
            // "chartScrollbar": {
            // },
            "chartCursor": {
                "cursorPosition": "mouse",
                "categoryBalloonDateFormat": "JJ:NN:SS",
            },
            "categoryField": "zeit",
            "categoryAxis": {
                "parseDates": true,
                "minPeriod": "ss",
                "axisColor": "#DADADA",
                "minHorizontalGap": 200, //welchen Abstand Zeitbeschriftungen haben
            },
            "export": {
                "enabled": true,
                "exportSelection": true,
                "exportTitles": true,
                "position": "bottom-right",
                "pageOrientation": "landscape",

            }
        });
        // chart.addListener("dataUpdated", zoomChart);
        // zoomChart();

        // function zoomChart() {
        //     chart.zoomToIndexes(chart.dataProvider.length - 20, chart.dataProvider.length - 1);
        // }
    }
    diagramm_data(generateChartData);

    /**
     * Set interval to push new data points periodically
     */
    // set up the chart to update every second
    setInterval(function () {
        function new_data(callback) {
            $.ajax({
                url: '/new_diagramm_data',
                type: 'GET',

                success: function (response) {
                    callback(response);
                }
            });
        }
        // mit den neuen Werten das Diagramm updaten
        function set_newChartData(chartData) {
            // console.log(chartData);
            // console.log(chart.dataProvider);
            // remove datapoint from the beginning
            chart.dataProvider.shift();
            // setze neue Daten ein
            chart.dataProvider.push(chartData);
            //updaten (und leider zoom verlieren...)
            chart.validateData();
        }
        new_data(set_newChartData);
    //    jede Sekunde updaten
    }, 5000);

});