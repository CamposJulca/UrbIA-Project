package urbia.utils;

import org.json.JSONArray;
import org.json.JSONObject;

import urbia.models.SensorReading;

import java.util.ArrayList;
import java.util.List;

public class JsonUtils {

    /**
     * Extrae lecturas desde un objeto JSON estructurado como el de ThingsBoard.
     * Retorna una lista de objetos SensorReading.
     */
    public static List<SensorReading> extraerLecturas(JSONObject json) {
        List<SensorReading> resultados = new ArrayList<>();

        for (String variable : json.keySet()) {
            JSONArray arr = json.optJSONArray(variable);
            if (arr != null) {
                for (int i = 0; i < arr.length(); i++) {
                    JSONObject obj = arr.getJSONObject(i);
                    long ts = obj.optLong("ts", 0L);
                    String valor = obj.optString("value", "0");
                    String fecha = DateFormatter.formatear(ts);

                    SensorReading lectura = new SensorReading(ts, variable, valor, fecha);
                    resultados.add(lectura);
                }
            }
        }

        return resultados;
    }
}
