package urbia.services;

import urbia.models.SensorReading;
import urbia.utils.HttpUtils;
import urbia.utils.DateFormatter;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class TelemetryService {

    private final String token;
    private final String baseUrl;

    public TelemetryService(String token) {
        this.token = token;
        this.baseUrl = System.getenv().getOrDefault("THINGSBOARD_URL", "http://localhost:8080") + "/api";
    }

    public List<SensorReading> obtenerLecturasRecientes(String deviceId) {
        List<SensorReading> lecturas = new ArrayList<>();
        String url = baseUrl + "/plugins/telemetry/DEVICE/" + deviceId + "/values/timeseries?limit=20";

        try {
            String response = HttpUtils.get(url, token);
            JSONObject json = new JSONObject(response);

            for (String clave : json.keySet()) {
                JSONArray array = json.getJSONArray(clave);
                for (int i = 0; i < array.length(); i++) {
                    JSONObject lectura = array.getJSONObject(i);
                    long timestamp = lectura.optLong("ts", 0L);
                    String valor = lectura.optString("value", "0");

                    SensorReading sr = new SensorReading(timestamp, clave, valor, DateFormatter.formatear(timestamp));
                    lecturas.add(sr);
                }
            }

        } catch (Exception e) {
            System.out.println("❌ Error al obtener telemetría: " + e.getMessage());
        }

        return lecturas;
    }
}
