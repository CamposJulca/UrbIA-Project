package urbia.services;

import urbia.models.DeviceInfo;
import urbia.utils.HttpUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class DeviceService {

    private final String token;
    private final String baseUrl;

    public DeviceService(String token) {
        this.token = token;
        this.baseUrl = System.getenv().getOrDefault("THINGSBOARD_URL", "http://localhost:8080") + "/api";
    }

    public List<DeviceInfo> obtenerDispositivos() {
        List<DeviceInfo> dispositivos = new ArrayList<>();

        try {
            String url = baseUrl + "/tenant/devices?pageSize=100&page=0";
            String response = HttpUtils.get(url, token);
            JSONObject json = new JSONObject(response);

            JSONArray data = json.optJSONArray("data");
            if (data == null || data.isEmpty()) {
                return dispositivos;
            }

            for (int i = 0; i < data.length(); i++) {
                JSONObject d = data.getJSONObject(i);
                String id = d.getJSONObject("id").getString("id");
                String name = d.getString("name");
                dispositivos.add(new DeviceInfo(id, name));
            }

        } catch (Exception e) {
            System.out.println("❌ Error al obtener dispositivos: " + e.getMessage());
        }

        return dispositivos;
    }
}
