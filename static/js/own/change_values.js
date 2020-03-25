/**
 * Created by Karsten on 18.04.2017.
 */


$(document).ready(function () {

    // Zahl eingeben
    $('.input_sollwert').bind("enterKey", function (e) {
        value = $(this).val();
        var id = $(this).attr('id');
        // console.log(value, id);
        $.ajax({
            url: '/sollwert',
            type: 'GET',
            data: {
                'value': value,
                'id': id
            },
            success: function (data) {
                console.log(data);
//              Neuen Wert ohne neu zu laden in aktuellen Wert schreiben
//              wenn Seite neu geladen wird, werden alle Werte in @app.route('/vorlage') auch neu geladen)
//              Zelle ueber ids: table und td_    schreibe value von data in Zelle
                $('table#table_input_sollwert td#td-' + id).html(data[id]);
            }
        });
    });
    // Bei Werteeingabe mit Enter abschliessen
    $('.input_sollwert').keyup(function (e) {
        if (e.keyCode == 13) {
            $(this).trigger("enterKey");
        }
    });

    // Zahl fuer Tabellen-Zeilenloeschung eingeben
    $('.input_table_rows').bind("enterKey", function (e) {
        value = $(this).val();
        var id = $(this).attr('id');
        $.ajax({
            url: '/input_table_rows',
            type: 'GET',
            data: {
                'value': value,
                'id': id
            },
            success: function (data) {
                // console.log(data);
//              Neuen Wert ohne neu zu laden in aktuellen Wert schreiben
//              wenn Seite neu geladen wird, werden alle Werte in @app.route('/vorlage') auch neu geladen)
//              Zelle ueber ids: table und td_    schreibe value von data in Zelle
                $('table#table_input_table_rows td#td-' + id).html(data[id]);
            }
        });
    });
    // Bei Werteeingabe mit Enter abschliessen
    $('.input_table_rows').keyup(function (e) {
        if (e.keyCode == 13) {
            $(this).trigger("enterKey");
        }
    });


    // Radio button choice k
    $('.radio_choice input:radio').click(function () {
        name = $(this).prop('name');
        value = $(this).val();
        console.log(name, value);

        // V2.00 Nachtrag: Truebung als 2. Vorlagebeschickungs-Ausloesung
        if (name == 'c_TOC_Trueb'){
            if (value == 1){
                console.log('Beschickungsvar1 aus');
                $('input:radio[name=Beschickungsvar]#Bes1').prop('disabled', true);
            }
            else{
                console.log('Beschickungsvar1 ein');
                $('input:radio[name=Beschickungsvar]#Bes1').prop('disabled', false);
            }
        }

        post_data = {'value': value, 'name': name};
        // Hier werden Daten von Javascript nur gesendet
        $.ajax({
            url: '/radio_choice',
            type: 'POST',
            data: {json_dict: JSON.stringify(post_data)},
            success: function (msg) {
                // console.log('radio_choice sent');
            }
        });
    });

    //Bools invertieren (in Python)
    $(".button_js").click(function () {
        value = $(this).val();
        var id = $(this).prop('id');
        $.ajax({
            url: '/change_bool',
            type: 'GET',
            data: {
                'value': value,
                'id': id
            },

            success: function (data) {
                try {
                    // falls Testbit nicht im Dict (irgend ein anderer Button wurde gedrueckt) -> weiter zu catch
                    dummy = "Testbit" in data;

                    // fuer Testbit
                    tb_name = 'Testbit';
                    var tb_val = data[tb_name];
                    var tb_id = $("div.monitor_meld#id-" + tb_name);
                    var snap7 = data['Snap7']
                    console.log(tb_name, tb_val, tb_id, snap7);

                    if (tb_val == 1) {
                        tb_id.addClass('btn-success').removeClass('btn-danger btn');
                        tb_id.html('Programm Online');
                        tb_id.show()
                        // nach 5 Sekunden verschwindet positive Meldung wieder
                        setTimeout(function () {
                            tb_id.hide();
                        }, 5000);
                    }
                    else if (tb_val == 0) {
                        tb_id.addClass('btn-danger btn').removeClass('btn-success');
                        tb_id.html('Programm nicht online, NEU STARTEN!');
                        tb_id.show();
                    }
                    //// Anzeige der classes
                    //var classList = tb_id.prop('class').split(/\s+/);
                    //console.log(classList);
                }

                catch (err) { // alle Befehle ausser Testbit
                    //console.log('Befehl gedrückt');
                }
            }//success

        });
    });
});
