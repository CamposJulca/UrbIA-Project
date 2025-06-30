package urbia.services;

import urbia.utils.HttpUtils;
import org.json.JSONObject;
import io.github.cdimascio.dotenv.Dotenv;

public class AuthService {

    private final String baseUrl;
    private final String username;
    private final String password;

    public AuthService() {
        Dotenv dotenv = Dotenv.load();  // Carga las variables desde .env
        this.baseUrl = dotenv.get("THINGSBOARD_URL") + "/api";
        this.username = dotenv.get("THINGSBOARD_USER");
        this.password = dotenv.get("THINGSBOARD_PASSWORD");
    }

    public String autenticar() {
        try {
            JSONObject payload = new JSONObject();
            payload.put("username", username);
            payload.put("password", password);

            String url = baseUrl + "/auth/login";
            String response = HttpUtils.post(url, payload.toString());

            JSONObject json = new JSONObject(response);
            String token = json.getString("token");

            System.out.println("✅ Autenticación exitosa.");
            return token;

        } catch (Exception e) {
            System.out.println("❌ Error al autenticar con ThingsBoard: " + e.getMessage());
            return null;
        }
    }
}
