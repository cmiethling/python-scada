/**
 * Created by Karsten on 01.05.2017.
 */

$(document).ready(function () {
//     $.ajax({
//             url: '/anlage_const_req',
//             type: 'GET',
//             success: function (data) {
//                   // console.log(data);
//                   // alert('get Mila');
// //
//             }
//         });

    //alle x millisec Werte aktualisieren
    $(function () {
        setInterval(function () {
            anlage_const_req();
            //testbit();
        }, 1000);
    });
    

    var anlage_const_req = function () {
        //nur fuer Bild: Anlage
        if (location.href == "http://127.0.0.1:5000/") {
            $.get("/anlage_const_req", function (data) {
                // console.log(data);
                // Messwerte
                mw = data[0];
                // Stoermeldungen
                st = data[1];
                // Betriebsmeldungen
                meld = data[2];


                //    Messwerte
                for (var k in mw) {
                    // use hasOwnProperty to filter out keys from the Object.prototype
                    if (mw.hasOwnProperty(k)) {
                        // k=key z.B fuer Vega1: $("div.monitor_val#id-Vega1").html(mw["Vega1"]);
                        $("div.monitor_val#id-" + k).html(mw[k]);
                    }
                }

                // Meldungen
                for (var k in meld) {
                    // use hasOwnProperty to filter out keys from the Object.prototype
                    if (meld.hasOwnProperty(k)) {
                        // console.log(k, meld[k]);
                        if (meld[k] == 0) {
                            $("div.monitor_meld#id-" + k).css({"backgroundColor": "gold"});
                        }
                        else if (meld[k] == 1) {
                            $("div.monitor_meld#id-" + k).css({"backgroundColor": "springgreen"});
                        }
                    }
                }

                // Stoermeldungen
                for (var k in st) {
                    // use hasOwnProperty to filter out keys from the Object.prototype
                    if (st.hasOwnProperty(k)) {
                        // console.log(k, st[k]);
                        if (st[k] == 0) {
                            $("div.monitor_meld#id-" + k).css({"backgroundColor": "transparent"});
                        }
                        else if (st[k] == 1) {
                            $("div.monitor_meld#id-" + k).css({"backgroundColor": "red"});
                        }
                    }
                }

            });
        }
    };



    //V3.00 Email-Benachrichtigung bei Sammelstoerung
    //180417 Von six_hour zu one_hour_interval_req

    /*
    last_value initialisieren -> wird eigentlich nur ein EINZIGES Mal ueberhaupt gemacht
    -> wenn last_value_stored_eternally das aller erste Mal in den Storage (vom Browser) geschrieben wird!
    https://stackoverflow.com/questions/16206322/how-to-get-js-variable-to-retain-value-after-page-refresh
    */
    if (localStorage.getItem("last_value_stored_eternally") == null){
        localStorage.setItem("last_value_stored_eternally", "false");
        console.log('last_value_stored_eternally initialiert!')
    };

    // Abfrage-Intervall
    $(function () {
        setInterval(function () {
    // 180417 Von six_hour zu one_hour_interval_req
            one_hour_interval_req();
        }, 1000*60*60); //in ms
    });

    var one_hour_interval_req = function () {
        // aus "last_value_stored_eternally" lesen
        var last_value = localStorage.getItem("last_value_stored_eternally");
        // console.log('last_value: ', last_value);
        $.ajax({
            url: '/one_hour_interval_req',
            type: 'GET',
            data: {
                'last_value': last_value
            },

            success: function (data) {// data in "last_value_stored_eternally" schreiben
                last_value = data;
                localStorage.setItem("last_value_stored_eternally", last_value);
                // console.log("new_value: ", localStorage.getItem("last_value_stored_eternally"));
            }//success

        });
    };

    /*
    var testbit = function () {
        $.get("/testbit", function (data) {
            // Testbit
            test = data;
            //    Testbit
            // console.log(test);
            $.each(test, function (k, val) {
                if (val == 0) {
                    $("div.monitor_meld#id-" + k).hide();
                }
                else if (val == 1) {
                    $("div.monitor_meld#id-" + k).show();
                }
            });
        });
    };
    **/

});