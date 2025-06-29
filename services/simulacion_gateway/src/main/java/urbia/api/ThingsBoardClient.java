package urbia.api; // ✅ Coincide con el path


import io.github.cdimascio.dotenv.Dotenv;
import urbia.models.SensorLectura;
import urbia.api.HttpUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.*;

public class ThingsBoardClient {
    private final String baseUrl;
    private final String username;
    private final String password;
    private String token;

    public ThingsBoardClient() {
        Dotenv dotenv = Dotenv.load();  // Carga el archivo .env automáticamente
        this.baseUrl = dotenv.get("THINGSBOARD_URL") + "/api";
        this.username = dotenv.get("THINGSBOARD_USER");
        this.password = dotenv.get("THINGSBOARD_PASSWORD");
    }

    public boolean autenticar() {
        try {
            JSONObject payload = new JSONObject();
            payload.put("username", username);
            payload.put("password", password);

            String response = HttpUtils.post(baseUrl + "/auth/login", payload.toString());
            JSONObject json = new JSONObject(response);
            token = json.getString("token");
            System.out.println("✅ Autenticación exitosa.");

            return true;
        } catch (Exception e) {
            System.out.println("❌ Error en autenticación: " + e.getMessage());
            return false;
        }
    }

    public List<Map<String, String>> obtenerDispositivos() {
        try {
            String response = HttpUtils.get(baseUrl + "/tenant/devices?pageSize=100&page=0", token);
            JSONObject json = new JSONObject(response);
            JSONArray data = json.getJSONArray("data");

            List<Map<String, String>> dispositivos = new ArrayList<>();
            for (int i = 0; i < data.length(); i++) {
                JSONObject obj = data.getJSONObject(i);
                Map<String, String> map = new HashMap<>();
                map.put("id", obj.getJSONObject("id").getString("id"));
                map.put("name", obj.getString("name"));
                dispositivos.add(map);
            }
            return dispositivos;
        } catch (Exception e) {
            System.out.println("❌ Error al obtener dispositivos: " + e.getMessage());
            return Collections.emptyList();
        }
    }

    public List<SensorLectura> obtenerLecturas(String deviceId) {
        try {
            String url = baseUrl + "/plugins/telemetry/DEVICE/" + deviceId + "/values/timeseries?limit=20";
            String response = HttpUtils.get(url, token);
            JSONObject json = new JSONObject(response);

            List<SensorLectura> lecturas = new ArrayList<>();
            for (String clave : json.keySet()) {
                JSONArray array = json.getJSONArray(clave);
                for (int i = 0; i < array.length(); i++) {
                    JSONObject obj = array.getJSONObject(i);
                    long ts = obj.getLong("ts");
                    String valor = obj.getString("value");
                    lecturas.add(new SensorLectura(ts, clave, valor));
                }
            }
            return lecturas;
        } catch (Exception e) {
            System.out.println("❌ Error al obtener lecturas: " + e.getMessage());
            return Collections.emptyList();
        }
    }
}
