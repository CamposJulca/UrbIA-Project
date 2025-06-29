package urbia.utils;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class JsonUtils {

    public static JSONObject parseJson(String json) {
        try {
            return new JSONObject(json);
        } catch (JSONException e) {
            System.out.println("❌ Error al parsear JSON: " + e.getMessage());
            return new JSONObject();
        }
    }

    public static List<Map<String, Object>> extraerLecturas(JSONObject json) {
        List<Map<String, Object>> resultados = new ArrayList<>();

        for (String variable : json.keySet()) {
            JSONArray arr = json.optJSONArray(variable);
            if (arr != null && arr.length() > 0) {
                JSONObject obj = arr.getJSONObject(0);
                long ts = obj.optLong("ts", 0L);
                Object value = obj.opt("value");

                Map<String, Object> lectura = new HashMap<>();
                lectura.put("variable", variable);
                lectura.put("valor", parseDouble(value));
                lectura.put("fecha", timestampToString(ts));
                resultados.add(lectura);
            }
        }

        return resultados;
    }

    private static String timestampToString(long timestamp) {
        if (timestamp == 0L) return "sin fecha";
        Instant instant = Instant.ofEpochMilli(timestamp);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
                .withZone(ZoneId.systemDefault());
        return formatter.format(instant);
    }

    private static double parseDouble(Object value) {
        if (value instanceof Number) {
            return ((Number) value).doubleValue();
        }
        try {
            return Double.parseDouble(value.toString());
        } catch (Exception e) {
            return 0.0;
        }
    }
}
